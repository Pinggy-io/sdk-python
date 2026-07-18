# Pinggy SDK 0.3.0

Targets **libpinggy 0.3.0**. Adds HAProxy PROXY-protocol support; existing
code is unaffected.

## Highlights

- **HAProxy PROXY protocol.** New `haproxy` option — set the
  PROXY-protocol version to send to your local server, which is expected to
  be a HAProxy (PROXY-protocol-aware) server so it sees the real client
  address. Use the `Tunnel.haproxy` property or the `haproxy=""` keyword on
  `pinggy.start_tunnel()`; an empty string (the default) disables it.
- **libpinggy 0.3.0.** The bundled native library is updated from 0.1.6.

---

# Pinggy SDK 0.1.0

This release rewires the Python SDK around **libpinggy 0.1.6**. The
shortcut entry points (`pinggy.start_tunnel` / `pinggy.start_udptunnel`)
keep their old signatures, so the most common usage pattern is
unchanged. Code that drove the explicit
`connect()` → `request_primary_forwarding()` → `serve_tunnel()`
lifecycle needs a small migration — see below.

## Highlights

- **Single-call lifecycle.** `tunnel.start()` does everything that the
  old three-step flow used to do. The old methods are still defined
  (no-ops) so existing code does not crash.
- **Multi-forwarding.** Configure several public bindings on one
  tunnel via `tunnel.add_forwarding(...)` or `tunnel.forwardings = …`.
- **Easier event handling.** Register callbacks without subclassing:

  ```python
  tunnel.on_tunnel_established = lambda urls: print(urls)
  tunnel.on_disconnected       = lambda msg:  print("bye:", msg)
  # or, for dynamic event names:
  tunnel.add_callback("tunnel_failed", on_failed)
  ```

- **Auto-reconnect, web debugger, usage updates, tunnel-state
  introspection** as first-class attributes.
- **`BaseTunnelHandler` refresh** — new `tunnel_established`,
  `tunnel_failed`, `forwardings_changed`, `disconnected`,
  `tunnel_error`, `will_reconnect`, `reconnecting`,
  `reconnection_completed`, `reconnection_failed`, `usage_update`
  callbacks. All string args arrive as `str`, list args as `list[str]`.
- **No more manual version edits.** Package version comes from git
  tags via `setuptools_scm` (`syncVersionWithTag.py` is gone).

## Migration in 30 seconds

Old:

```python
tunnel = pinggy.Tunnel()
tunnel.tcp_forward_to = "localhost:8080"
tunnel.connect()
tunnel.request_primary_forwarding()
print(tunnel.urls)
tunnel.serve_tunnel()
```

New:

```python
tunnel = pinggy.Tunnel()
tunnel.add_forwarding("localhost:8080")
tunnel.start(thread=True)
print(tunnel.urls)        # populated once forwarding is up
tunnel.wait()
```

If you used `pinggy.start_tunnel(...)`, you do not need to change
anything — the signature is backwards-compatible.

## Notable bug fixes

- `pinggy.start_udptunnel()` works again — was crashing with
  `AttributeError` in 0.0.20 (reversed argument order, lost
  `eventclass`).
- A second `tunnel.start()` no longer raises
  `Synchronization error` (lock was never released).
- `tunnel_failed` / `tunnel_error` callbacks now receive `str`, not
  `bytes`.
- Failed native-library load no longer cascades into a confusing
  `AttributeError` in `Tunnel.__del__`.

## Breaking changes

- `BaseTunnelHandler.additional_forwarding_succeeded` /
  `additional_forwarding_failed` gained a `forwardingType` parameter.
- The legacy lifecycle callbacks (`authenticated`,
  `authentication_failed`, `primary_forwarding_succeeded`,
  `primary_forwarding_failed`) no longer fire — the underlying C
  library merged the steps. Use `tunnel_established` /
  `tunnel_failed` instead.
- Mixing legacy properties (`tcp_forward_to`, `type`, `udp_*`) with
  the new `forwardings` / `add_forwarding` API on the same `Tunnel`
  raises an exception. Pick one style per tunnel.

## Other

- CI now runs unit tests on Linux, macOS, and Windows in parallel
  before building wheels.
- Action versions bumped to Node.js 24-supporting majors.

For the full list, see [`CHANGELOG.md`](./CHANGELOG.md).
