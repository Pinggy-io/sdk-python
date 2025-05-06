# Documentation for `pinggy`

## Class `BaseTunnelHandler`

Represent basic and default handler for :class:`Tunnel`. It provide default handler
for various event triggered by the Tunnel. It is expected that all the event handler
would extend this event handler.

### `BaseTunnelHandler.additional_forwarding_failed(self, bindAddr, forwardTo, err)`

Triggers when additional forwarding fails

### `BaseTunnelHandler.additional_forwarding_succeeded(self, bindAddr, forwardTo)`

Triggers when additional forwarding completes successfully. Learn more at
https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.

**This is experimental and not tested**

Agrs:
    bindAddr (str): remote address where connection can be sent.
    forwardTo (str): address to which connection would forwarded. It is equivalen to `tcp_forward_to`.

### `BaseTunnelHandler.authenticated(self)`

Triggers when tunnel successfully authenticated. Authentication happen even for free tunnels.

### `BaseTunnelHandler.authentication_failed(self, errors)`

Triggers when tunnel could not able to authenticate it self. Reasons are provided in the `errors` argument.
Any further action on the tunnel object will fail.

**Arguments**:
- **errors (list(str))**: Authentication failure reasons.

### `BaseTunnelHandler.disconnected(self, msg)`

Triggers when tunnel got disconnected by the server.

Agrs:
    msg (str): disconnection reason.

### `BaseTunnelHandler.get_tunnel(self)`

Returns the tunnel object
**Returns**:
- **Tunnel**: the tunnel object

### `BaseTunnelHandler.handle_channel(self)`

**Do not return anything but False**

### `BaseTunnelHandler.new_channel(self, channel: pinggy.pylib.Channel)`

**Do not use**

### `BaseTunnelHandler.primary_forwarding_failed(self, msg)`

Triggers when primary (or default) forwarding fails. The reason is present in the msg.

Agrs:
    msg (str): the reason why it failes.

### `BaseTunnelHandler.primary_forwarding_succeeded(self)`

Triggers when primary (or default) forwarding successfully completed.
Know more about primary (or default) forwarding at
https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.

Once this step done, one can fetch the urls from the tunnel.

### `BaseTunnelHandler.tunnel_error(self, errorNo, msg, recoverable)`

In case some error occures. Errors could be recoverable.

**Arguments**:
- **errorNo (int)**: internal error no. Currently not useful for user.
- **msg (str)**: description
- **recoverable (bool)**: whether a error is recoverable or not. Application should ignore recoverable errors.

## Class `Tunnel`

The primary class which provides the tunnel.

There are two simple way to start a tunnel. If we want to forward local apache server listening on
port 80 to the internet we can start tunnel via following:

Example 1:

    >>> import pinggy
    >>> tunnel = pinggy.Tunnel()
    >>> tunnel.tcp_forward_to = "localhost:80"
    >>> tunnel.start()

Example 2:

    >>> import pinggy
    >>> tunnel = pinggy.Tunnel()
    >>> tunnel.tcp_forward_to = "localhost:80"
    >>> tunnel.connect()
    >>> tunnel.request_primary_forwarding()
    >>> tunnel.serve_tunnel()

There several configuration available, that one might need to consider.

Flow 1:

    > Create Tunnel
    >         |
    >         |-> set attributes
    >         |
    >         |-> connect() -> authentication failed callback
    >         |       |
    >         |       `-> authentication success callback
    >         |
    >         |-> request_primary_forwarding() -> primary forwarding failed callback
    >         |       |
    >         |       `-> primary forwarding succeeded callback
    >         |
    >         |-> request_additional_forwarding(bindaddress, forwardto) -> additional forwarding failed callback
    >         |       |
    >         |       `-> additional forwarding succeeded callback
    >         |
    >         `-> serve_tunnel()

Flow 2:

    > Create Tunnel
    >         |
    >         |-> set attributes
    >         |
    >         |-> start() -> authentication failed callback
    >                 |
    >                 `-> authentication success callback -> primary forwarding failed callback
    >                             |
    >                             `-> primary forwarding succeeded callback

### `Tunnel.advanced_parsing`

keep it true. Free tunnels won't work without it.

### `Tunnel.argument`

str: tunnel arguments for header manipulation and others.

### `Tunnel.connect(self)`

Connect the tunnel with the server and authenticate it self. It returns true on success.

If this step fails, no futher step steps can be continued.

**Returns**:
- **bool**: whether authentication done sucessfully or not.

### `Tunnel.force`

bool: force flag in tunnel that terminates any existing tunnel with the same token.

### `Tunnel.insecure`

*No docstring provided.*

### `Tunnel.is_active(self)`

Check if tunnel is active or not.

### `Tunnel.request_additional_forwarding(self, bindAddr, forwardTo)`

Once primary forwarding is done, user can request additional forwarding for other ports.

More details at: https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.

### `Tunnel.request_primary_forwarding(self)`

Request to start the default forwarding. Once suceeded, user can get
the urls and tunnel starts accepting requests.

### `Tunnel.serve_tunnel(self)`

Final method in the tunnel creation flow. It is again a blocking call.

### `Tunnel.server_address`

str: pinggy server address. The default server address is `a.pinggy.io`. You can also add the
    port as follows: `a.pinggy.io:443`.

### `Tunnel.sni_server_name`

*No docstring provided.*

### `Tunnel.ssl`

*No docstring provided.*

### `Tunnel.start(self)`

Start the tunnel with the provided configuration. This is a blocking call.
It does not return unless tunnel stopped externally or some error occures.

### `Tunnel.start_web_debugging(self, port=4300)`

Start the web debugger. All the request would be handled internally.

Call this function after primary forwarding completed successfully.

### `Tunnel.start_with_c(self)`

** DO NOT USE THIS METHOD **

### `Tunnel.stop(self)`

Stops the running tunnel.

### `Tunnel.tcp_forward_to`

str: local server address for default or primary forward. It is equivalent to -R option in ssh

Example:
    If local server is running at port 8080. Forward request to it by setting

    >>> tunnel.tcp_forward_to = "localhost:8080"

### `Tunnel.token`

str: Token for the tunnel. One can it from `dashboard.pinggy.io`

### `Tunnel.type`

str: Tunnel type or mode. This is only for TCP type. So, the accepted values are 'http',
    'tcp', 'tls' and 'tlstcp'. Default is 'http'.

### `Tunnel.udp_forward_to`

str: Similar to `tcp_forward_to`. However, it is for udp tunnel.

### `Tunnel.udp_type`

str: Tunnel type or mode. This is only for UDP type. currently, only accepted value is 'udp'.

### `Tunnel.urls`

list(str): lists of public urls for the running tunnel (read only)

### `build_os()`

Get the detail about the build operating system.

**Returns**:
- **str**: os detail.

### `build_timestamp()`

Function to get the build timestamp as per the build-system.

**Returns**:
- **str**: build timestamp.

### `disableLog()`

Disable logging by the native library.

### `git_commit()`

Function to get the git commit hash of the source code.

**Returns**:
- **str**: git commit hash.

### `libc_version()`

Get the libc version of the native. This information is accurate only for linux operating system.

**Returns**:
- **str**: libc version.

### `setLogPath(path)`

Set path where native library print its log. Use this function only if requires.
To disable native library logging completly, use `disableLog` function.

### `version()`

Function to know the native library version.

**Returns**:
- **str**: libpinggy version.

