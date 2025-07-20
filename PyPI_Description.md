# Pinggy

*A powerful Python library for creating and managing network tunnels with easy-to-use functionality for HTTP, TCP, TLS, and UDP tunneling.*

Pinggy is a versatile library designed for creating secure tunnels between local and remote servers. It supports HTTP, TCP, TLS, and UDP tunneling, making it ideal for use cases such as port forwarding, secure connections, multi-port tunneling, and advanced debugging. With support for authentication, advanced configuration, and error handling, Pinggy is an excellent choice for network diagnostics, server debugging, and remote access tasks.

## Features

- **Supports multiple tunneling protocols**: HTTP, TCP, TLS, and UDP.
- **Comprehensive event handling**: Extend `BaseTunnelHandler` for custom authentication, connection, forwarding, and error events.
- **Multi-port forwarding**: Easily manage primary and additional port forwarding requests.
- **Authentication support**: Includes Basic Authentication, Bearer Authentication, and IP whitelisting.
- **Web Debugger**: Start a web debugger on a custom port to capture tunnel traffic.
- **Header modification**: Add, remove, or update request headers dynamically.
- **Reverse Proxy & TLS**: Enable/disable reverse proxy mode and local server TLS (with SNI support).
- **Asynchronous Operation**: Manage tunnels without blocking other operations.
- **Simple API**: Create, configure, and manage tunnels with just a few lines of code.

## Installation

To install Pinggy, simply run:

```
pip install pinggy
```

## Quick Start Guide

Use the `start_tunnel` function to quickly set up and start a tunnel with minimal code.

### Example 1: Start an HTTP Tunnel (Basic Usage)

```
import pinggy

# Start an HTTP tunnel forwarding traffic to localhost on port 8080
tunnel = pinggy.start_tunnel(forwardto="localhost:8080", token="your_token_here")

print(f"Tunnel started with token: {tunnel.token}")
```

### Example 2: Start a TCP Tunnel with Custom Authentication and IP Whitelisting

```
import pinggy

tunnel = pinggy.start_tunnel(
    forwardto="localhost:80",
    token="your_token_here",
    force=True,
    ipwhitelist=["192.168.1.100", "23.15.30.223"],
    type="tcp"
)

print(f"TCP Tunnel started at {tunnel.server_address} with token: {tunnel.token}")
```

### Example 3: Start a UDP Tunnel with Web Debugger

```
import pinggy

tunnel = pinggy.start_tunnel(
    forwardto="localhost:53",
    token="your_token_here",
    type="udp",
    webdebuggerport=4300
)

print(f"UDP Tunnel started with web debugger at port 4300")
```

### Example 4: Advanced Configuration (TLS, Headers, Reverse Proxy)

```
import pinggy

tunnel = pinggy.start_tunnel(
    forwardto="localhost:443",
    token="your_token_here",
    type="tls",
    localservertls=True,  # Enable TLS for local server
    headermodification=["a:X-Test:Value", "r:User-Agent"],
    reverseproxy=False
)

print(f"TLS Tunnel started with custom headers and reverse proxy disabled.")
```

## Key Methods & Properties

- `start_tunnel()`: Starts a tunnel with the provided configuration and options (type, token, port forwarding, TLS, authentication, etc.).
- `start_udptunnel()`: Starts a UDP tunnel with similar configuration options.
- `Tunnel.start()`: Starts the tunnel in a blocking manner.
- `Tunnel.connect()`: Connects the tunnel and performs authentication.
- `Tunnel.request_primary_forwarding()`: Requests the primary forwarding for the tunnel.
- `Tunnel.request_additional_forwarding()`: Adds additional port forwarding after the primary forwarding is complete.
- `Tunnel.stop()`: Stops the tunnel.
- `Tunnel.is_active()`: Checks if the tunnel is currently active.
- `Tunnel.urls`: Lists public URLs for the running tunnel.
- `Tunnel.xff`, `Tunnel.httpsonly`, `Tunnel.fullrequesturl`, `Tunnel.allowpreflight`, `Tunnel.reverseproxy`, `Tunnel.localservertls`, `Tunnel.headermodification`, `Tunnel.basicauth`, `Tunnel.bearerauth`, `Tunnel.ipwhitelist`, `Tunnel.token`, `Tunnel.type`, `Tunnel.tcp_forward_to`, `Tunnel.udp_forward_to`, `Tunnel.sni_server_name`, `Tunnel.force`, `Tunnel.argument`.

## Advanced Features

- **Web Debugger**: Start a debugger on a custom port to inspect tunnel traffic.
- **Authentication Options**: Use basic authentication, bearer tokens, or IP whitelisting for secure access.
- **Reverse Proxy & TLS**: Enable/disable reverse proxy mode and local server TLS (with SNI support).
- **Header Modification**: Add, remove, or update request headers dynamically.
- **Multi-port Forwarding**: Easily manage primary and additional port forwarding requests.
- **Comprehensive Event Handling**: Extend `BaseTunnelHandler` for custom event handling (authentication, forwarding, errors, etc.).

## Documentation

For more details on usage and configuration, visit the full documentation at <https://pinggy.io/docs>.

## Contributing

We welcome contributions to the Pinggy library! Feel free to fork the repository, report bugs, or submit pull requests.

## License

Pinggy is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
