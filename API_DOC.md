# Pinggy SDK — API Reference

A hand-curated reference for the public surface of the `pinggy` package.
For a quick-start overview see the
[PyPI description](./PyPI_Description.md); for product-level concepts see
<https://pinggy.io/docs>.

> Anything not documented here (legacy `tcp_forward_to` / `udp_forward_to`
> properties, `connect` / `request_primary_forwarding` / `serve_tunnel`
> methods, `Channel` class, `advanced_parsing`, `insecure`, `ssl`,
> `sni_server_name`, etc.) is either internal or kept only as a
> compatibility shim for code written against pre-0.1.0 releases. Do not
> rely on it for new development.

## Contents

- [Shortcut functions](#shortcut-functions)
  - [`start_tunnel`](#start_tunnel)
  - [`start_udptunnel`](#start_udptunnel)
- [`Tunnel`](#tunnel)
  - [Constructor](#constructor)
  - [Lifecycle](#lifecycle)
  - [Forwardings](#forwardings)
  - [URLs and state](#urls-and-state)
  - [Authentication and access control](#authentication-and-access-control)
  - [HTTP request behaviour](#http-request-behaviour)
  - [Header rewriting](#header-rewriting)
  - [Local-server TLS](#local-server-tls)
  - [Web debugger](#web-debugger)
  - [Auto-reconnect](#auto-reconnect)
  - [Usage updates](#usage-updates)
  - [Server greeting](#server-greeting)
  - [Per-event callbacks](#per-event-callbacks)
- [`BaseTunnelHandler`](#basetunnelhandler)
- [`TunnelState`](#tunnelstate)
- [Exceptions](#exceptions)
- [Logging and version helpers](#logging-and-version-helpers)

---

## Shortcut functions

The two `start_*` helpers build a `Tunnel`, configure it from kwargs, and
launch it in a background thread. Each blocks until the tunnel is
established (so `tunnel.urls` is populated) or raises `RuntimeError` if
the tunnel fails to start.

### `start_tunnel`

```python
pinggy.start_tunnel(
    forwardto = 80,
    type = "http",
    token = "",
    force = False,
    ipwhitelist = None,
    basicauth = None,
    bearerauth = None,
    headermodification = None,
    webdebuggerport = 0,
    xff = False,
    httpsonly = False,
    fullrequesturl = False,
    allowpreflight = False,
    reverseproxy = True,
    serveraddress = "a.pinggy.io:443",
    udpforwardto = None,
    localservertls = False,
    autoreconnect = False,
    eventclass = BaseTunnelHandler,
) -> Tunnel
```

| Argument             | Type                                | Default              | Description                                                                                                                                          |
| -------------------- | ----------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `forwardto`          | `int \| str`                        | `80`                 | Local destination. Accepts a port (`8080`), `"host:port"`, or `"schema://host:port"` (schemas: `http`, `https`, `tcp`, `tls`, `tlstcp`, `udp`).      |
| `type`               | `str`                               | `"http"`             | Tunnel type. One of `http`, `tcp`, `tls`, `tlstcp`, `udp`.                                                                                            |
| `token`              | `str`                               | `""`                 | Pinggy access token (from <https://dashboard.pinggy.io>). Required for paid features.                                                                |
| `force`              | `bool`                              | `False`              | Stop any existing tunnel that uses the same token before connecting.                                                                                  |
| `ipwhitelist`        | `list[str] \| str`                  | `None`               | IPv4/IPv6 addresses or CIDRs allowed to reach the tunnel.                                                                                            |
| `basicauth`          | `dict[str, str]`                    | `None`               | `{username: password}` map for HTTP Basic Auth.                                                                                                      |
| `bearerauth`         | `list[str] \| str`                  | `None`               | Accepted bearer tokens. May be combined with `basicauth`.                                                                                            |
| `headermodification` | `list[dict] \| list[str]`           | `None`               | Header rewrite rules (HTTP only). See [header rewriting](#header-rewriting).                                                                          |
| `webdebuggerport`    | `int`                               | `0`                  | Port for the local web debugger UI. `0` disables it.                                                                                                  |
| `xff`                | `bool`                              | `False`              | Add `X-Forwarded-For` to forwarded requests.                                                                                                          |
| `httpsonly`          | `bool`                              | `False`              | Reject plain-HTTP connections; redirect to HTTPS.                                                                                                    |
| `fullrequesturl`     | `bool`                              | `False`              | Add `X-Pinggy-Url` carrying the original request URL.                                                                                                |
| `allowpreflight`     | `bool`                              | `False`              | Let CORS preflight requests through without auth.                                                                                                    |
| `reverseproxy`       | `bool`                              | `True`               | When `False`, forward the original `Host` header to the upstream instead of rewriting it.                                                            |
| `serveraddress`      | `str`                               | `"a.pinggy.io:443"`  | Pinggy edge server.                                                                                                                                  |
| `udpforwardto`       | `int \| str`                        | `None`               | Add a parallel UDP forwarding alongside the primary (TCP/HTTP/TLS) one.                                                                              |
| `localservertls`     | `bool \| str`                       | `False`              | Speak TLS to the local upstream. `True` uses SNI `localhost`; pass a string to override the SNI name.                                                |
| `autoreconnect`      | `bool`                              | `False`              | Reconnect automatically on transient drops.                                                                                                          |
| `eventclass`         | subclass of `BaseTunnelHandler`     | `BaseTunnelHandler`  | Handler class instantiated for the tunnel. Override its methods, or use `tunnel.add_callback(...)` / `tunnel.on_<event> = ...` instead of subclassing. |

**Returns:** a started `Tunnel`. Raises `RuntimeError` if the tunnel fails to start.

### `start_udptunnel`

```python
pinggy.start_udptunnel(
    forwardto,
    token = "",
    force = False,
    ipwhitelist = None,
    webdebuggerport = 4300,
    serveraddress = "a.pinggy.io:443",
    autoreconnect = False,
    eventclass = BaseTunnelHandler,
) -> Tunnel
```

UDP-only convenience wrapper. Arguments behave the same as in
`start_tunnel`. Use `start_tunnel(..., udpforwardto=...)` when you need
both UDP and a primary TCP/HTTP/TLS forwarding on the same tunnel.

---

## `Tunnel`

Lower-level handle. Build it manually when you need more control than the
shortcuts offer (multiple forwardings, callback registration without a
handler subclass, dynamic reconfiguration before `start()`, etc.).

### Constructor

```python
pinggy.Tunnel(
    server_address = "a.pinggy.io:443",
    eventClass = BaseTunnelHandler,
)
```

| Argument         | Type                              | Default              | Description                                       |
| ---------------- | --------------------------------- | -------------------- | ------------------------------------------------- |
| `server_address` | `str`                             | `"a.pinggy.io:443"`  | Pinggy edge server.                               |
| `eventClass`     | subclass of `BaseTunnelHandler`   | `BaseTunnelHandler`  | Class instantiated and bound to this tunnel.      |

A fresh `Tunnel` is in `Initial` state; configure it, then call
[`start()`](#lifecycle).

### Lifecycle

| Member                                                  | Description                                                                                                                                                                                                                                  |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `start(thread=False, block_until_ready=True)`           | Start the tunnel. With `thread=False` blocks for the entire tunnel lifetime. With `thread=True` runs the tunnel on a worker; by default still blocks until the tunnel is established or fails (raises `RuntimeError`). Pass `block_until_ready=False` to return as soon as the worker is launched. |
| `wait()`                                                | Block until the worker thread exits. Safe no-op if the tunnel was started synchronously.                                                                                                                                                      |
| `stop()`                                                | Stop the tunnel. Joins the worker thread if called from a different thread.                                                                                                                                                                   |
| `is_active() -> bool`                                   | Whether the tunnel is currently alive.                                                                                                                                                                                                        |

After `start()` succeeds, configuration setters raise — reconfigure on a
new `Tunnel`.

### Forwardings

A tunnel must have at least one *primary* forwarding. The first
`add_forwarding` call (or the `forwardings` setter) creates the primary;
subsequent calls add *additional* forwardings.

| Member                                                                  | Description                                                                                                                                                                          |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `add_forwarding(address, type=None, listen_address=None)`               | Add a forwarding rule. `address` accepts `"port"`, `":port"`, `"host:port"`, or `"schema://host:port"`. `type` is one of `http`/`tcp`/`tls`/`tlstcp`/`udp` (default `http`). `listen_address` is the optional remote bind on the Pinggy server (`"host"`, `"host:port"`, or `":port"`). |
| `forwardings` *(property)*                                              | Get the current forwardings as a JSON string. Set with a single address (`str` / `int`) or a list of dicts (`{"address": ..., "type": ..., "listenAddress": ...}`). Cannot be mixed with `add_forwarding` after the tunnel is started. |

### URLs and state

| Member                          | Description                                                                                          |
| ------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `urls` *(read-only property)*   | List of public URLs assigned by the server once the tunnel is established. Empty before that point.   |
| `state` *(read-only property)*  | Current `pinggy.pylib.TunnelState` value (see [`TunnelState`](#tunnelstate)).                         |
| `server_address` *(property)*   | Pinggy edge server `host:port`.                                                                       |

### Authentication and access control

| Member                                | Description                                                                              |
| ------------------------------------- | ---------------------------------------------------------------------------------------- |
| `token` *(property)*                  | Pinggy access token. Required for paid features.                                          |
| `force` *(property)*                  | Stop any existing tunnel using the same token at connect time.                            |
| `basicauth` *(property)*              | `{username: password}` map (or list of single-pair dicts) for HTTP Basic Auth.            |
| `bearerauth` *(property)*             | List of accepted bearer tokens (or a single string).                                      |
| `ipwhitelist` *(property)*            | List of IPs / CIDRs allowed to reach the tunnel.                                          |

### HTTP request behaviour

These flags only affect HTTP-type tunnels.

| Member                              | Description                                                                                                          |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `xff` *(bool property)*             | Add `X-Forwarded-For`.                                                                                              |
| `httpsonly` *(bool property)*       | Reject plain HTTP; redirect to HTTPS.                                                                                |
| `fullrequesturl` *(bool property)*  | Add `X-Pinggy-Url` carrying the original full request URL.                                                          |
| `allowpreflight` *(bool property)*  | Let CORS preflight requests through without authentication.                                                          |
| `reverseproxy` *(bool property)*    | Default `True` (rewrite `Host` to the upstream's). Set `False` to forward the original `Host` instead.                |

### Header rewriting

| Member                                       | Description                                                                                                                                                          |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `headermodification` *(property)*            | Full list of header rules. Accepts a list of dicts (`{"type": "add"\|"update"\|"remove", "key": ..., "value": [...]}`) or a list of shorthand strings (`"a:Key:Val"`, `"u:Key:Val"`, `"r:Key"`). |
| `add_header(name, value)`                    | Append an `add` rule.                                                                                                                                                |
| `update_header(name, value)`                 | Append an `update` rule.                                                                                                                                             |
| `remove_header(name)`                        | Append a `remove` rule.                                                                                                                                              |

See <https://pinggy.io/docs/advanced/live_header/> for semantics.

### Local-server TLS

| Member                              | Description                                                                                                                            |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `localservertls` *(property)*       | Speak TLS to the local upstream. Set to a string to use it as the SNI name; set to a truthy non-string to default to `"localhost"`.    |

### Web debugger

| Member                                       | Description                                                                                                                                                                                |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `webdebugger` *(bool property)*              | Enable the local debugger UI.                                                                                                                                                              |
| `webdebugger_addr` *(property)*              | Bind address (`host:port`) for the debugger UI. Setting `webdebugger_port` rewrites this to `localhost:<port>`.                                                                            |
| `webdebugger_port` *(property)*              | Bind port for the debugger UI. Sets `webdebugger_addr` to `localhost:<port>`.                                                                                                              |
| `start_web_debugging(port=4300)`             | Start the debugger after the tunnel is up (alternative to setting the property before `start()`).                                                                                          |

### Auto-reconnect

| Member                                  | Description                                                                              |
| --------------------------------------- | ---------------------------------------------------------------------------------------- |
| `auto_reconnect` *(bool property)*      | Reconnect automatically on transient disconnects.                                         |
| `max_reconnect_attempts` *(int)*        | Upper bound on retries. `0` means infinite.                                               |
| `reconnect_interval` *(float, seconds)* | Delay between retries.                                                                    |

### Usage updates

When enabled, the server periodically pushes traffic-usage data via the
`usage_update` event.

| Member                       | Description                                                                                          |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| `start_usage_update()`       | Subscribe to usage push events.                                                                       |
| `stop_usage_update()`        | Unsubscribe.                                                                                         |
| `current_usages` *(property)*| Current usage snapshot polled from the native library. Returns a parsed `dict`, or `None` if unavailable. |

### Server greeting

| Member                            | Description                                                              |
| --------------------------------- | ------------------------------------------------------------------------ |
| `greeting_msgs` *(read-only)*     | Greeting strings sent by the server after the tunnel is established.      |

### Per-event callbacks

Either subclass [`BaseTunnelHandler`](#basetunnelhandler) and pass the
class via `eventClass=` / `eventclass=`, or attach callables directly to
the tunnel:

```python
tunnel.on_tunnel_established = lambda urls: print("up:", urls)
tunnel.on_disconnected       = lambda msg:  print("bye:", msg)

# Equivalent dynamic form:
tunnel.add_callback("tunnel_failed", lambda msg: print("failed:", msg))
```

A callback registered on the tunnel takes precedence over a method of
the same name on the handler class.

| Member                                              | Description                                                                                                                                  |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `add_callback(event_name, callback)`                | Attach a callback for any handler-method name. Equivalent to `tunnel.on_<event_name> = callback`, but lets you pick the name at runtime.       |
| `on_<event>` *(properties)*                         | Property aliases for the events listed under [`BaseTunnelHandler`](#basetunnelhandler) (e.g. `on_tunnel_established`, `on_disconnected`, …).   |

---

## `BaseTunnelHandler`

Subclass and override the methods you care about. All string arguments
arrive as `str` (utf-8 decoded); list arguments arrive as `list[str]`.

```python
class BaseTunnelHandler:
    def get_tunnel(self) -> Tunnel
```

| Event method                                                            | Fires when                                                                                                          |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `tunnel_established(urls)`                                              | The tunnel and its primary forwarding are up. `urls` is a list of public URLs.                                       |
| `tunnel_failed(msg)`                                                    | The handshake or initial forwarding fails. `msg` describes the failure.                                              |
| `forwardings_changed(forwarding)`                                       | The set of active forwardings changed (e.g. an additional forwarding was added or removed).                          |
| `additional_forwarding_succeeded(bind_addr, forward_to, forwarding_type)` | An additional forwarding was accepted by the server.                                                                  |
| `additional_forwarding_failed(bind_addr, forward_to, forwarding_type, error)` | An additional forwarding was rejected by the server.                                                                  |
| `disconnected(msg)`                                                     | The server closed the tunnel. `msg` carries the disconnect reason.                                                   |
| `tunnel_error(error_no, msg, recoverable)`                              | Internal SDK / library error. `recoverable=True` means the SDK will attempt to recover; safe for the app to ignore.   |
| `will_reconnect(messages)`                                              | Auto-reconnect is enabled and the SDK is about to start retrying.                                                    |
| `reconnecting(retry_cnt)`                                               | A reconnect attempt is starting. `retry_cnt` is the 1-based attempt number.                                          |
| `reconnection_completed()`                                              | A new tunnel is established after a reconnect.                                                                       |
| `reconnection_failed(retry_cnt)`                                        | All reconnect attempts have been exhausted; this is unrecoverable.                                                  |
| `usage_update(usages)`                                                  | The server pushed a new usage snapshot. Requires `start_usage_update()`.                                             |

`get_tunnel()` returns the bound `Tunnel`.

---

## `TunnelState`

`pinggy.pylib.TunnelState` (an `enum.Enum`) is what `Tunnel.state`
returns. Values:

| Name                  | Meaning                                                                                |
| --------------------- | -------------------------------------------------------------------------------------- |
| `Invalid`             | Tunnel object is in an unusable state.                                                  |
| `Initial`             | Constructed but not started.                                                            |
| `Started`             | `start()` has been called.                                                              |
| `Connecting`          | Establishing the underlying TCP/TLS connection.                                         |
| `Connected`           | Underlying connection is up; protocol handshake has not run yet.                        |
| `SessionInitiating`   | Negotiating the Pinggy session.                                                         |
| `SessionInitiated`    | Pinggy session is ready.                                                                |
| `Authenticating`      | Authenticating the user/token.                                                          |
| `Authenticated`       | Authentication succeeded.                                                               |
| `ForwardingInitiated` | Requesting the primary forwarding.                                                      |
| `ForwardingSucceeded` | Forwarding active; this corresponds to the `tunnel_established` event.                  |
| `ReconnectInitiated`  | A reconnect cycle has begun.                                                            |
| `Reconnecting`        | Currently retrying.                                                                     |
| `Stopped`             | `stop()` has been called.                                                               |
| `Ended`               | Tunnel terminated; no further callbacks will fire.                                      |

---

## Exceptions

| Exception                          | Raised when                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| `pinggy.PinggyNativeLoaderError`   | The native `libpinggy` shared library cannot be located or loaded.                    |
| `pinggy.PinggyRemovedPropertyError`| A property that no longer exists in the current SDK version is accessed.              |

`Tunnel.start()` (and the `start_*` shortcuts) also raise built-in
`RuntimeError` if `block_until_ready=True` and the tunnel fails to come
up.

---

## Logging and version helpers

Module-level functions on `pinggy`:

| Function                 | Description                                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| `set_log_path(path)`     | Redirect native-library logs to `path`. The path must be writable.                                      |
| `disable_log()`          | Suppress native-library logs entirely.                                                                  |
| `enable_log()`           | Re-enable native-library logs after `disable_log()`.                                                    |
| `version()`              | `libpinggy` library version string.                                                                     |
| `git_commit()`           | Git commit hash baked into the native library.                                                          |
| `build_timestamp()`      | Build timestamp of the native library.                                                                  |
| `libc_version()`         | Linker / libc version reported by the native library (Linux only; placeholder on other platforms).      |
| `build_os()`             | Build-host OS string for the native library.                                                            |

The legacy camel-case spellings `setLogPath` / `disableLog` are kept as
aliases for `set_log_path` / `disable_log`. Prefer the snake-case names
in new code.
