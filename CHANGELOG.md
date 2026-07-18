# Changelog

## 0.3.0

Targets **libpinggy 0.3.0** (up from 0.1.6).

### Highlights

- **HAProxy PROXY protocol**: new `haproxy` option — set the
  PROXY-protocol version to send to the local server, which is expected to
  be a HAProxy (PROXY-protocol-aware) server so it receives the real client
  address. Available as the `Tunnel.haproxy` property and as a `haproxy=""`
  keyword on `pinggy.start_tunnel()`; an empty string (the default)
  disables it.
- **libpinggy 0.3.0**: the bundled native library is updated from 0.1.6 to
  0.3.0.

---

## 0.1.0

`pinggy` 0.1.0 targets **libpinggy 0.1.6** and rewrites a large part of the
SDK around the new C library. Most user code that uses
`pinggy.start_tunnel()` / `pinggy.start_udptunnel()` keeps working — those
shortcut signatures are intentionally backwards-compatible. Code that drove
the old explicit lifecycle (`tunnel.connect()` →
`tunnel.request_primary_forwarding()` → `tunnel.serve_tunnel()`) needs a
small adjustment, described below.

### Highlights

- **One-call lifecycle**: `tunnel.start()` does the whole thing —
  authenticate, set up forwarding, serve. The previous staged
  `connect()` / `request_primary_forwarding()` / `serve_tunnel()` flow is
  no longer needed (the methods stay around as no-ops so old code does
  not crash, but they are not documented and have no effect).
- **Multi-forwarding API**: `tunnel.forwardings = …` and
  `tunnel.add_forwarding(address, type=…, listen_address=…)` replace the
  old single `tcp_forward_to` / `udp_forward_to` properties. The old
  properties still work as a legacy compat shim, but they cannot be
  mixed with the new API on the same `Tunnel`.
- **New event handler**: `BaseTunnelHandler` has a fresh set of methods
  (`tunnel_established`, `tunnel_failed`, `forwardings_changed`,
  `disconnected`, `tunnel_error`, `will_reconnect`, `reconnecting`,
  `reconnection_completed`, `reconnection_failed`, `usage_update`,
  plus updated `additional_forwarding_*`).
- **Callbacks without subclassing**: register a function for any event
  with `tunnel.add_callback("tunnel_established", fn)` or simply
  `tunnel.on_tunnel_established = fn`.
- **Auto-reconnect**, **web debugger**, **usage updates**, and
  **tunnel-state introspection** are first-class features.
- **Versioning**: package version now comes from git tags via
  `setuptools_scm`. No more manual edits to `__version__.py`.

---

### Quick migration

#### Old code (0.0.20)

```python
import pinggy

tunnel = pinggy.Tunnel()
tunnel.tcp_forward_to = "localhost:8080"
tunnel.connect()
tunnel.request_primary_forwarding()
print("URLs:", tunnel.urls)
tunnel.serve_tunnel()
```

#### New code (0.1.0)

```python
import pinggy

tunnel = pinggy.Tunnel()
tunnel.add_forwarding("localhost:8080")
tunnel.start(thread=True)        # returns; blocks if thread=False
print("URLs:", tunnel.urls)      # populated once tunnel is established
tunnel.wait()                    # block until the tunnel ends
```

The shortcut function still works the same:

```python
tunnel = pinggy.start_tunnel(forwardto="localhost:8080", token="…")
```

---

### Breaking changes

- **`BaseTunnelHandler.additional_forwarding_succeeded` and
  `additional_forwarding_failed` gained a `forwardingType` argument**:

  ```python
  # 0.0.20
  def additional_forwarding_succeeded(self, bindAddr, forwardTo): ...
  def additional_forwarding_failed   (self, bindAddr, forwardTo, err): ...

  # 0.1.0
  def additional_forwarding_succeeded(self, bindAddr, forwardTo, forwardingType): ...
  def additional_forwarding_failed   (self, bindAddr, forwardTo, forwardingType, err): ...
  ```
- **The old per-step lifecycle callbacks are no longer fired** — the C
  library merged the steps. The methods are still defined as empty
  stubs on `BaseTunnelHandler` so subclasses calling
  `super().<callback>()` do not crash, but they will never be invoked
  by the SDK:

  - `authenticated()`
  - `authentication_failed(errors)`
  - `primary_forwarding_succeeded()`
  - `primary_forwarding_failed(msg)`

  Use the new combined events instead:

  | Old callback                        | New callback                     |
  | ----------------------------------- | -------------------------------- |
  | `authenticated`                     | `tunnel_established(urls)`       |
  | `primary_forwarding_succeeded`      | `tunnel_established(urls)`       |
  | `authentication_failed(errors)`     | `tunnel_failed(msg)`             |
  | `primary_forwarding_failed(msg)`    | `tunnel_failed(msg)`             |

- **Mixing legacy and new forwarding properties on the same `Tunnel`
  raises** an exception. Pick one style per `Tunnel`:

  ```python
  # OK — all legacy
  tun.tcp_forward_to = "localhost:8080"

  # OK — all new
  tun.add_forwarding("localhost:8080", type="tcp")

  # ❌ raises
  tun.tcp_forward_to = "localhost:8080"
  tun.add_forwarding(":9090")
  ```

---

### New API

#### `Tunnel`

- `tunnel.start(thread=False)` — single entry point; pass `thread=True`
  to run the tunnel in a background thread.
- `tunnel.wait()` — block until the tunnel ends (use after
  `start(thread=True)`).
- `tunnel.add_forwarding(address, type=None, listen_address=None)` —
  add a forwarding rule (primary or additional).
- `tunnel.forwardings` — get/set the full forwarding list as a string
  or list of dicts.
- `tunnel.add_callback(event_name, callback)` and per-event properties
  (`tunnel.on_tunnel_established`, `tunnel.on_disconnected`, …) —
  register callbacks without subclassing `BaseTunnelHandler`.
- `tunnel.add_header(name, value)`, `remove_header(name)`,
  `update_header(name, value)`.
- `tunnel.auto_reconnect`, `max_reconnect_attempts`,
  `reconnect_interval`.
- `tunnel.webdebugger`, `webdebugger_addr`, `webdebugger_port`.
- `tunnel.start_usage_update()`, `stop_usage_update()`,
  `current_usages`.
- `tunnel.greeting_msgs` — server greeting strings (after the tunnel
  is established).
- `tunnel.state` — current `TunnelState` enum value.

#### Shortcut functions

- `pinggy.start_tunnel(...)` — backward-compatible signature; new
  optional kwargs added at the end:

  - `udpforwardto` — open a parallel UDP forwarding alongside the
    primary one.
  - `localservertls` — `True`, `False`, or an SNI string. Enables
    local-server TLS for the upstream.
  - `autoreconnect` — survive transient disconnects.
  - `eventclass` — pass a `BaseTunnelHandler` subclass.

- `pinggy.start_udptunnel(...)` — backward-compatible; `autoreconnect`
  and `eventclass` added.

#### `BaseTunnelHandler` callbacks (override what you need)

```python
class MyHandler(pinggy.BaseTunnelHandler):
    def tunnel_established(self, urls):                      ...
    def tunnel_failed(self, msg):                            ...
    def forwardings_changed(self, url_map):                  ...
    def additional_forwarding_succeeded(self, bind_addr, forward_to_addr, forwarding_type): ...
    def additional_forwarding_failed   (self, bind_addr, forward_to_addr, forwarding_type, error): ...
    def disconnected(self, error):                           ...
    def tunnel_error(self, error_no, error, recoverable):    ...
    def will_reconnect(self, messages):                      ...
    def reconnecting(self, retry_cnt):                       ...
    def reconnection_completed(self):                        ...
    def reconnection_failed(self, retry_cnt):                ...
    def usage_update(self, usages):                          ...
```

All callback string arguments arrive as `str` (utf-8 decoded);
list-style arguments arrive as `list[str]`.

#### Exposed types and exceptions

- `pinggy.TunnelState` — enum reflecting the libpinggy state machine
  (`Initial`, `Connecting`, `Authenticated`,
  `ForwardingSucceeded`, `Stopped`, `Ended`, …).
- `pinggy.PinggyRemovedPropertyError` — raised by removed properties.

---

### Bug fixes

- **`start_udptunnel` was completely broken** in 0.0.20 (its internal
  `add_forwarding` call was reversed; it raised `AttributeError`
  before reaching the server, and silently dropped the user's
  `eventclass`). Both fixed.
- **A second call to `Tunnel.start()` raised `Synchronization error`**
  because the internal lock was never released (missing parens on
  `self.__lock.release`). Fixed.
- **`Tunnel.__del__` could raise `AttributeError`** if the native
  library failed to load before the constructor finished. Now safe.
- **`tunnel_failed` and `tunnel_error` user callbacks received raw
  bytes** instead of `str`. Now decoded.
- **`add_forwarding` with an `int` port** (e.g.
  `tun.add_forwarding(8080)`) is accepted — coerced to
  `localhost:<port>` for parity with the `forwardings` setter.

---

### Deprecated (still works, undocumented)

These names exist only so old user code does not crash. Do not rely on
them for new development.

- Methods on `Tunnel`: `connect()`, `request_primary_forwarding()`,
  `serve_tunnel()`, `start_with_c()`.
- Properties on `Tunnel`: `tcp_forward_to`, `udp_forward_to`, `type`,
  `udp_type`.
- Empty stubs on `BaseTunnelHandler`: `authenticated`,
  `authentication_failed`, `primary_forwarding_succeeded`,
  `primary_forwarding_failed`.

---

### Build, packaging, CI

- **Versioning**: `pinggy/__version__.py` no longer holds a hardcoded
  string. `setuptools_scm` reads the latest git tag at build time and
  writes a generated `pinggy/_version.py` (gitignored). Tagging
  `v0.1.0` produces a `pinggy-0.1.0` wheel; commits past the tag get
  an automatic dev suffix like `0.1.0.dev3+g<sha>`. The
  `syncVersionWithTag.py` helper has been removed.
- **CI** (`.github/workflows/build.yml`):
  - Runs unit tests on `ubuntu-latest`, `macos-latest`, and
    `windows-latest` in parallel; the wheel-build step depends on
    them passing.
  - Triggers on every push (any branch).
  - Action versions bumped to ones that ship Node.js 24
    (`actions/checkout@v6`, `actions/setup-python@v6`,
    `actions/upload-artifact@v7`).
- **Internal refactors** (no user-visible API impact):
  - `core.py` callback wrappers auto-decode `bytes → str` and
    collapse `(length, char_p_p)` argument pairs into `list[str]` so
    `pylib.py` callbacks deal in Python natives.
  - `core.py` setters skip redundant manual `str → bytes` encoding —
    handled centrally by the existing wrapper.
  - Dispatcher parameter names aligned with the C typedefs in
    `pinggy.h`.
  - Typo fix: `tunnel_statup_messages` → `tunnel_startup_messages`.
