# Documentation for `pinggy`

## Class `BaseTunnelHandler`

Represent basic and default handler for :class:`Tunnel`. It provide default handler
for various event triggered by the Tunnel. It is expected that all the event handler
would extend this event handler.

### `BaseTunnelHandler.additional_forwarding_failed(self, bindAddr, forwardTo, forwardingType, err)`

Triggers when additional forwarding fails

### `BaseTunnelHandler.additional_forwarding_succeeded(self, bindAddr, forwardTo, forwardingType)`

Triggers when additional forwarding completes successfully. Learn more at
https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.

**This is experimental and not well tested**

Agrs:
    bindAddr (str): remote address where connection can be sent.
    forwardTo (str): address to which connection would forwarded. It is equivalen to `tcp_forward_to`.

### `BaseTunnelHandler.disconnected(self, msg)`

Triggers when tunnel got disconnected by the server.

Agrs:
    msg (str): disconnection reason.

### `BaseTunnelHandler.forwardings_changed(self, forwarding)`

Triggeres whenever some changes happens to the forwarding list. It basically contains list of mappings between
public url and local forwarding. This function primarily triggers everytime some forwarding completed successfully.

### `BaseTunnelHandler.get_tunnel(self)`

Returns the tunnel object
**Returns**:
- **Tunnel**: the tunnel object

### `BaseTunnelHandler.handle_channel(self)`

**Do not return anything but False**

### `BaseTunnelHandler.new_channel(self, channel: pinggy.pylib.Channel)`

**Do not use**

### `BaseTunnelHandler.reconnecting(self, retry_cnt)`

Triggers whenever sdk tries to reconnect the tunnel.

### `BaseTunnelHandler.reconnection_completed(self)`

Triggers whenever new tunnel established.

### `BaseTunnelHandler.reconnection_failed(self, retry_cnt)`

Triggers when the sdk exhaust reconnect attempt and unable to connect at all. This is an unrecoverable error.

### `BaseTunnelHandler.tunnel_error(self, errorNo, msg, recoverable)`

In case some error occures. Errors could be recoverable.

**Arguments**:
- **errorNo (int)**: internal error no. Currently not useful for user.
- **msg (str)**: description
- **recoverable (bool)**: whether a error is recoverable or not. Application should ignore recoverable errors.

### `BaseTunnelHandler.tunnel_established(self, url: list[str])`

Triggers when pre-configured forwardings are successfully completed.
Know more about forwarding at
https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.

Once this step done, one can fetch the urls from the tunnel.

### `BaseTunnelHandler.tunnel_failed(self, msg)`

Triggers when pre-configured forwardings are failed. The reason is present in the msg.

Agrs:
    msg (str): the reason why it failed.

### `BaseTunnelHandler.usage_update(self, usages)`

Server provides usages update to the client. Application have to turn it on by calling `start_usage_update` function

### `BaseTunnelHandler.will_reconnect(self, messages)`

Triggers when existing tunnel drops and it is configured to reconnect automatically.

## Class `PinggyNativeLoaderError`

Common base class for all non-exit exceptions.

## Class `PinggyRemovedPropertyError`

Raised when accessing a removed property.

## Class `Tunnel`

The primary class which provides the tunnel.

There are two simple way to start a tunnel. If we want to forward local apache server listening on
port 80 to the internet we can start tunnel via following:

Example 1:

    >>> import pinggy
    >>> tunnel = pinggy.Tunnel()
    >>> tunnel.forwardings = "localhost:80"
    >>> tunnel.start(True)
    >>> tunnel.urls

Example 2:

    >>> import pinggy
    >>> tunnel = pinggy.Tunnel()
    >>> tunnel.forwardings = "localhost:80"
    >>> tunnel.start()

### `Tunnel.add_forwarding(self, address: str, type: str | None = None, listen_address: str | None = None)`

Adds a new forwarding rule to the tunnel configuration.

This function allows you to specify how incoming connections to a remote `listen_address`
on the Pinggy server should be forwarded to a local `address` on your local machine.

**Arguments**:
- **address (str)**: The local address to forward to.
  This can be a URL (e.g., "http://localhost:3000"), an IP address
  (e.g., "127.0.0.1:8000"), or just a port (e.g., ":5000").
  If the schema (e.g., "http://") and host are omitted, "localhost"
  is assumed. For example, ":3000" becomes "http://localhost:3000"
  for HTTP forwarding.
  If `type` is "http" and `address` specifies an "https"
  schema (e.g., "https://localhost:443"), this implicitly enables
  `local_server_tls` for this specific forwarding rule.

- **type (str, optional)**: The type of forwarding.
  Valid types are "http", "tcp", "udp", "tls", "tlstcp".
  If an empty string or None is provided, "http" is assumed.

- **listen_address (str, optional)**: The remote address to bind to.
  This can be a domain name, a domain:port combination,
  or just a port. Examples: "example.pinggy.io",
  "example.pinggy.io:8080", ":80".
  If empty string or None, the server will assign a default binding.
  The hostname is ignored for TCP and UDP tunnels.
  Any schema provided will be ignored.

Examples:
    >>> tunnel.add_forwarding(address="localhost:8000")

### `Tunnel.add_header(self, header_name, new_value)`

*No docstring provided.*

### `Tunnel.advanced_parsing`

keep it true. Free tunnels won't work without it.

### `Tunnel.allowpreflight`

bool: allow preflight requests to pass through without processing

### `Tunnel.argument`

str: tunnel arguments for header manipulation and others.

### `Tunnel.auto_reconnect`

Set auto_reconnecting tunnel. It is required for long running tunnel.

### `Tunnel.basicauth`

dict[str, str]|None: List of username and correstponding password.

### `Tunnel.bearerauth`

list[str]|None: list of key for bearer authentication

### `Tunnel.current_usages`

Get the usage.

### `Tunnel.force`

bool: force flag in tunnel that terminates any existing tunnel with the same token.

### `Tunnel.forwardings`

Retrieves the forwarding rules (as a JSON string) from the tunnel config.

### `Tunnel.fullrequesturl`

bool: request full url. if this flag is set, full original url would be pass through `X-Pinggy-Url` header in the request

### `Tunnel.greeting_msgs`

Get the greeting msg for the tunnel. This can be retrieved only after tunnel establishment.

### `Tunnel.headermodification`

list[str]|None: list of header modifications. Check https://pinggy.io/docs/advanced/live_header/ for more details

### `Tunnel.httpsonly`

bool: whether https only is set or not

### `Tunnel.insecure`

Keep it true. Production tunnel doesn't works without it.

### `Tunnel.ipwhitelist`

list[str]|None: List of IP/IP ranges that allowed to connect to the tunnel. SDK does not verify the IP

### `Tunnel.is_active(self)`

Check if tunnel is active or not.

### `Tunnel.localservertls`

str: return current localservertls config,

### `Tunnel.max_reconnect_attempts`

Set number of connection attempt before it give up. Setting this to `0` means infinite attempts.

### `Tunnel.reconnect_interval`

Set the interval in seconds between two reconnection attempts.

### `Tunnel.remove_header(self, header_name)`

*No docstring provided.*

### `Tunnel.request_additional_forwarding(self, bindAddr, forwardTo, forwardingType='http')`

Once primary forwarding is done, user can request additional forwarding for other ports.

More details at: https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.

### `Tunnel.reverseproxy`

"bool: enables reverseproxy mode. default is true.

### `Tunnel.server_address`

str: pinggy server address. The default server address is `a.pinggy.io`. You can also add the
    port as follows: `a.pinggy.io:443`.

### `Tunnel.sni_server_name`

Do not modify unless instructed by the pinggy developers.

### `Tunnel.ssl`

Keep it true. Production tunnel doesn't works without ssl.

### `Tunnel.start(self, thread=False)`

Start the tunnel with the provided configuration. This is a blocking call.
It does not return unless tunnel stopped externally or some error occures.

**Arguments**:
- **thread (bool)**: Whether to run the start tunnel in a new thread. Default is False

### `Tunnel.start_usage_update(self)`

Start usage update. It would start puching update via the callback

### `Tunnel.start_web_debugging(self, port=4300)`

Start the web debugger. All the request would be handled internally.

Call this function after primary forwarding completed successfully.

### `Tunnel.state`

libpinggy maintain states for each tunnels. Application can fetch these state for its own use.

### `Tunnel.stop(self)`

Stops the running tunnel.

### `Tunnel.stop_usage_update(self)`

Stop usages update.

### `Tunnel.token`

str: Token for the tunnel. One can it from `dashboard.pinggy.io`

### `Tunnel.update_header(self, header_name, new_value)`

*No docstring provided.*

### `Tunnel.urls`

list(str): lists of public urls for the running tunnel (read only)

### `Tunnel.wait(self)`

Wait for tunnel to stop. It does not stop the tunnel though.

### `Tunnel.webdebugger`

*No docstring provided.*

### `Tunnel.webdebugger_addr`

*No docstring provided.*

### `Tunnel.webdebugger_port`

*No docstring provided.*

### `Tunnel.xff`

bool: whethere xff is set or not.

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

### `disable_log()`

Disable logging by the native library.

### `enable_log()`

Enable libpinggy log.

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

**Arguments**:
- **path (str)**: New log path. Path needs to have write permission.

### `set_log_path(path)`

Set path where native library print its log. Use this function only if requires.
To disable native library logging completly, use `disableLog` function.

**Arguments**:
- **path (str)**: New log path. Path needs to have write permission.

### `start_tunnel(forwardto: int | str = 80, type: str = 'http', token: str = '', force: bool = False, ipwhitelist: list[str] | str | None = None, basicauth: dict[str, str] | None = None, bearerauth: list[str] | str | None = None, headermodification: list[str] | None = None, webdebuggerport: int = 0, xff: bool = False, httpsonly: bool = False, fullrequesturl: bool = False, allowpreflight: bool = False, reverseproxy: bool = True, serveraddress: str = 'a.pinggy.io:443', udpforwardto: int | str | None = None, localservertls: str | bool = False, autoreconnect: bool = False, eventclass=<class 'pinggy.pylib.BaseTunnelHandler'>)`

Start a tunnel inside a new thread and get reference to the tunnel.

**Arguments**:
- **forwardto**: address of local server. Only port can be provided incase of local server. Example: 80, "localhost:80".
  The format is [schema://][localhost:]port. Schema can be one of `http`, `https`, `tcp`, `tls`, `tlstcp`, `udp`. Default is `http`.
  `https` means local server tls.

- **type**: Type of tunnel. One of `http`, `tcp`, `tls`, `tlstcp`, `udp`. Default is `http`.

- **token**: User token. Get it from https://dashboard.pinggy.io

- **force**: enable of disable force flag. Enabling it would cause to stop any existing tunnel with same token.

- **ipwhitelist**: list of ipaddresses that are allowed to connect to the tunnel. Example: ["2301::c4f:45c2:57e6:e637:7f1a/128","23.15.30.223/32"].
  Be carefull about the ipv6 syntax

- **basicauth**: dictionary of username:password. This dictionary be used for basic authentication. Example: {"hello": "world"}

- **bearerauth**: list of keys that would be used for bearer key authentication. Both basicauth and bearerauth can be used together.
  Example: ["1234"]

- **headermodification**: list of header modification that would be added. More detail at https://pinggy.io/docs/advanced/live_header/
  Example: [{"type": "remove", "key": "Accept"}, {"type": "update", "key": "UserAgent", "value" :["PinggyTestServer 1.2.3"]}], ["r:Accept", "u:UserAgent:PinggyTestServer 1.2.3"]

- **webdebuggerport**: Webdebugging port. Webdebugging would start only if valid port is provided. Example: 4300

- **localservertls**: This flag enables TLS for the local server. If it is a string, it would be used as the server name for SNI. If it is True, it would be set to "localhost" by default.
  If it is False, it would be set to None. Default: False

- **xff**: With this flag, pinggy adds `X-Forwarded-For` with the request header.

- **httpsonly**: This flag make sure that the visitor uses only the https. Any request to http would the redirected to https url.

- **fullrequesturl**: Pinggy server adds the original url that is requested in a header `X-Pinggy-Url ` with the request.

- **allowpreflight**: With this flag, pinggy detects and allow preflight request without processing so that the server can handle it.

- **reverseproxy**: Pinggy by default runs in reverse proxy mode. However, it can be turned off by setting this flag `False`

- **serveraddress**: User can set the server address to which pinggy would connect. Default: `a.pinggy.io:443`.

- **udpforwardto**: same as forwardto, however, it forwards a UDP destination alongside the primary forwarding.
  Useful when one tunnel needs to expose both TCP and UDP. Use `start_udptunnel` for udp-only tunnels.

- **autoreconnect**: automatically reconnects when tunnel failes. It happens silently. So, to detect reconnection, one need to override the event handler.

- **eventclass**: event handler class. Object would be created for the tunnel.

### `start_udptunnel(forwardto: int | str, token: str = '', force: bool = False, ipwhitelist: list[str] | str | None = None, webdebuggerport: int = 4300, serveraddress: str = 'a.pinggy.io:443', autoreconnect: bool = False, eventclass=<class 'pinggy.pylib.BaseTunnelHandler'>)`

Start an udp tunnel inside a new thread and get reference to the tunnel.

**Arguments**:
- **forwardto**: address of local server. Only port can be provided incase of local server. Example: 53, "localhost:53".

- **token**: User token. Get it from https://dashboard.pinggy.io

- **force**: enable of disable force flag. Enabling it would cause to stop any existing tunnel with same token.

- **ipwhitelist**: list of ipaddresses that are allowed to connect to the tunnel. Example: ["2301::c4f:45c2:57e6:e637:7f1a/128","23.15.30.223/32"].

- **webdebuggerport**: Webdebugging port. Webdebugging would start only if valid port is provided. Example: 4300

- **serveraddress**: User can set the server address to which pinggy would connect. Default: `a.pinggy.io:443`.

- **autoreconnect**: automatically reconnects when tunnel failes. It happens silently. So, to detect reconnection, one need to override the event handler.

- **eventclass**: event handler class. Object would be created for the tunnel.

### `version()`

Function to know the native library version.

**Returns**:
- **str**: libpinggy version.

