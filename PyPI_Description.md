
# Pinggy

*A powerful Python library for creating and managing network tunnels with easy-to-use functionality for HTTP, TCP, and UDP tunneling.*

Pinggy is a versatile library designed for creating secure tunnels between local and remote servers. It supports HTTP, TCP, and UDP tunneling, making it ideal for use cases such as port forwarding, secure connections, or even multi-port tunneling. With support for authentication, advanced configuration, and error handling, Pinggy is an excellent choice for network diagnostics, server debugging, and remote access tasks.

## Features

- **Supports multiple tunneling protocols**: HTTP, TCP, TLS, and UDP.

- **Comprehensive event handling**: Automatic handling of authentication, connection issues, and forwarding events.

- **Multi-port forwarding**: Easily manage primary and additional port forwarding requests.

- **Authentication support**: Includes Basic Authentication, Bearer Authentication, and IP whitelisting.

- **Web Debugger**: Start a web debugger on a custom port to capture tunnel traffic.

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

# The tunnel will start in the background and handle traffic to the specified port
print(f"Tunnel started with token: {tunnel.token}")
```

### Example 2: Start a TCP Tunnel with Custom Authentication and IP Whitelisting

```
import pinggy

# Start a TCP tunnel with custom configuration
tunnel = pinggy.start_tunnel(
    forwardto="localhost:80",                 # Forward to localhost on port 80
    token="your_token_here",                  # Authentication token
    force=True,                               # Force stop any existing tunnel with the same token
    ipwhitelist=["192.168.1.100", "23.15.30.223"],  # Allowed IPs
    type="tcp"                                # Tunnel type (TCP in this case)
)

# The tunnel will start in the background, and the specified configuration will be applied
print(f"TCP Tunnel started at {tunnel.server_address} with token: {tunnel.token}")
```

### Example 3: Start a UDP Tunnel with Web Debugger

```
import pinggy

# Start a UDP tunnel with a web debugger enabled
tunnel = pinggy.start_tunnel(
    forwardto="localhost:53",                  # Forward UDP traffic to localhost on port 53
    token="your_token_here",                   # Authentication token
    type="udp",                                # Tunnel type (UDP in this case)
    webdebuggerport=4300                       # Start web debugger on port 4300
)

# The tunnel will start in the background, and you can access the web debugger on port 4300
print(f"UDP Tunnel started with web debugger at port 4300")
```

## Key Methods

- `start_tunnel()`: Starts a tunnel with the provided configuration and options (e.g., type, token, port forwarding).

- `Tunnel.start()`: Starts the tunnel in a blocking manner.

- `Tunnel.connect()`: Connects the tunnel and performs authentication.

- `Tunnel.request_primary_forwarding()`: Requests the primary forwarding for the tunnel.

- `Tunnel.request_additional_forwarding()`: Adds additional port forwarding after the primary forwarding is complete.

- `Tunnel.stop()`: Stops the tunnel.

- `Tunnel.is_active()`: Checks if the tunnel is currently active.

## Advanced Features

- **Web Debugger**: Start a debugger on a custom port to inspect tunnel traffic.

- **Authentication Options**: Use basic authentication, bearer tokens, or IP whitelisting for secure access.

- **Reverse Proxy Mode**: Default reverse proxy mode can be disabled via configuration.

## Documentation

For more details on usage and configuration, visit the full documentation at <https://pinggy.io/docs>.

## Contributing

We welcome contributions to the Pinggy library! Feel free to fork the repository, report bugs, or submit pull requests.

## License

Pinggy is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
