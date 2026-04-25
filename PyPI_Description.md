# Pinggy

*A Python SDK for [Pinggy](https://pinggy.io) — create and manage HTTP, TCP, TLS, and UDP tunnels from your code.*

Pinggy lets you expose a local server to the internet through a secure tunnel without changing your application. The Python SDK wraps the native `libpinggy` library and gives you a small, ergonomic API for everything Pinggy supports: multi-port forwarding, basic / bearer / IP-whitelist auth, header rewriting, web debugging, auto-reconnect, and more.

## Features

- **Multiple protocols**: HTTP, TCP, TLS, TLS-over-TCP, and UDP.
- **Multi-port forwarding**: declare several public bindings on a single tunnel.
- **Authentication**: Basic Auth, Bearer tokens, and IP whitelisting.
- **Header rewriting**: add, remove, or update request headers on the fly.
- **Web debugger**: inspect every request flowing through the tunnel.
- **Reverse proxy & local TLS**: control whether the tunnel rewrites Host / SNI for the upstream.
- **Auto-reconnect**: configurable retry behaviour for long-running tunnels.
- **Event handlers**: subclass `BaseTunnelHandler` to react to lifecycle events (forwardings, disconnect, reconnect, usage updates, …).

## Installation

```bash
pip install pinggy
```

## Quick start

The fastest way to spin up a tunnel is `pinggy.start_tunnel`. It builds a tunnel on a background thread and returns a handle you can query.

### HTTP tunnel

```python
import pinggy

tunnel = pinggy.start_tunnel(forwardto="localhost:8080")
print("Public URLs:", tunnel.urls)

tunnel.wait()  # block until the tunnel ends
```

### Authenticated TCP tunnel with IP whitelist

```python
import pinggy

tunnel = pinggy.start_tunnel(
    forwardto="localhost:22",
    type="tcp",
    token="your_token_here",
    force=True,
    ipwhitelist=["192.168.1.100", "23.15.30.223/32"],
)
print("Public TCP URLs:", tunnel.urls)
```

### UDP tunnel with web debugger

```python
import pinggy

tunnel = pinggy.start_udptunnel(
    forwardto="localhost:53",
    token="your_token_here",
    webdebuggerport=4300,
)
print("Public UDP URLs:", tunnel.urls)
```

### Local TLS, header rewriting, reverse proxy off

```python
import pinggy

tunnel = pinggy.start_tunnel(
    forwardto="localhost:443",
    type="tls",
    token="your_token_here",
    localservertls=True,
    headermodification=[
        {"type": "remove", "key": "Accept"},
        {"type": "update", "key": "User-Agent", "value": ["PinggyTestServer 1.2.3"]},
    ],
    reverseproxy=False,
)
```

## Lower-level API

If you need finer control, build a `Tunnel` directly. Configure it via attributes / `add_forwarding`, then call `start()`.

```python
import pinggy

tunnel = pinggy.Tunnel(server_address="a.pinggy.io:443")
tunnel.token = "your_token_here"
tunnel.add_forwarding("localhost:8080")                  # primary HTTP forwarding
tunnel.add_forwarding("localhost:8443", type="tls")      # additional forwarding
tunnel.auto_reconnect = True
tunnel.start(thread=True)

print(tunnel.urls)
tunnel.wait()
```

### Reacting to events

Override the methods on `BaseTunnelHandler` you care about and pass the class to the tunnel:

```python
import pinggy

class MyHandler(pinggy.BaseTunnelHandler):
    def tunnel_established(self, urls):
        print("Tunnel up:", urls)

    def tunnel_failed(self, msg):
        print("Tunnel failed:", msg)

    def disconnected(self, msg):
        print("Disconnected:", msg)

tunnel = pinggy.start_tunnel(forwardto=8080, eventclass=MyHandler)
tunnel.wait()
```

## Key API surface

| Function / class                       | Purpose                                                                |
|----------------------------------------|------------------------------------------------------------------------|
| `pinggy.start_tunnel(...)`             | Convenience: build, configure, and start a tunnel in one call.         |
| `pinggy.start_udptunnel(...)`          | Same, for UDP-only tunnels.                                            |
| `pinggy.Tunnel(...)`                   | Low-level tunnel object — configure attributes then `start()`.         |
| `pinggy.BaseTunnelHandler`             | Base class for event handlers.                                         |
| `Tunnel.add_forwarding(address, ...)`  | Add a forwarding rule (primary or additional).                         |
| `Tunnel.forwardings`                   | Get / set all forwardings as a string or list of dicts.                |
| `Tunnel.start(thread=False)`           | Start the tunnel; pass `thread=True` to run it in the background.      |
| `Tunnel.stop()`                        | Stop a running tunnel.                                                 |
| `Tunnel.urls`                          | Public URLs assigned by the server.                                    |
| `Tunnel.is_active()`                   | Whether the tunnel is currently active.                                |
| `Tunnel.start_web_debugging(port)`     | Enable the web debugger on a port after forwarding succeeds.           |

## Documentation

Full SDK reference: see `API_DOC.md` in the source tree.
Pinggy product docs: <https://pinggy.io/docs>.

## License

Apache 2.0. See `LICENSE`.
