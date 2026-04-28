# Pinggy

[![PyPI](https://img.shields.io/pypi/v/pinggy.svg)](https://pypi.org/project/pinggy/)
[![Python versions](https://img.shields.io/pypi/pyversions/pinggy.svg)](https://pypi.org/project/pinggy/)
[![License](https://img.shields.io/pypi/l/pinggy.svg)](https://github.com/Pinggy-io/sdk-python/blob/main/LICENSE)

Official Python SDK for [Pinggy](https://pinggy.io) — expose a local server
to the public internet through a managed tunnel. Wraps the native
`libpinggy` library with a small, ergonomic API.

Supports HTTP, TCP, TLS, TLS-over-TCP, and UDP tunnels with multi-port
forwarding, authentication, header rewriting, a built-in web debugger, and
auto-reconnect.

## Installation

```bash
pip install pinggy
```

Wheels for Linux, macOS, and Windows bundle the native `libpinggy` library
— no extra setup required. Python 3.6+.

## Quick start

```python
import pinggy

tunnel = pinggy.start_tunnel(forwardto="localhost:8080")
print("Public URLs:", tunnel.urls)

tunnel.wait()  # block until the tunnel ends
```

`start_tunnel()` runs the tunnel in a background thread and blocks until
the tunnel is established (so `tunnel.urls` is populated) or raises
`RuntimeError` if it fails to start.

For a TCP tunnel, an authenticated tunnel, or any other configuration,
pass the relevant kwargs:

```python
tunnel = pinggy.start_tunnel(
    forwardto="localhost:22",
    type="tcp",
    token="your_token_here",
)
```

## Reacting to events

Either subclass `BaseTunnelHandler`:

```python
class MyHandler(pinggy.BaseTunnelHandler):
    def tunnel_established(self, urls):
        print("Tunnel up:", urls)
    def disconnected(self, msg):
        print("Disconnected:", msg)

tunnel = pinggy.start_tunnel(forwardto=8080, eventclass=MyHandler)
tunnel.wait()
```

…or register callbacks directly on the tunnel:

```python
import pinggy

tunnel = pinggy.Tunnel()
tunnel.add_forwarding("localhost:8080")

tunnel.on_tunnel_established = lambda urls: print("Tunnel up:", urls)
tunnel.on_disconnected       = lambda msg:  print("Disconnected:", msg)

tunnel.start(thread=True)
tunnel.wait()
```

## Documentation

- **API reference** — [`API_DOC.md`](https://github.com/Pinggy-io/sdk-python/blob/main/API_DOC.md)
- **Pinggy product docs** — <https://pinggy.io/docs>
- **Changelog** — [`CHANGELOG.md`](https://github.com/Pinggy-io/sdk-python/blob/main/CHANGELOG.md)
- **Source / issues** — <https://github.com/Pinggy-io/sdk-python>

## License

Apache 2.0. See [`LICENSE`](https://github.com/Pinggy-io/sdk-python/blob/main/LICENSE).
