import errno
import ctypes
import threading
import shlex
import threading
import json
from enum import Enum
import logging
import typing

logger = logging.getLogger(__name__)

from . import pinggyexception

try:
    from . import core
except pinggyexception.PinggyNativeLoaderError as e:
    class DummyCore:
        def __init__(self, e):
            self.loading_exception = e
        def disable_sdk_log(self):
            pass
        def __getattr__(self, name):
                raise self.loading_exception

        def __call__(self, *args, **kwargs):
            raise self.loading_exception

    core = DummyCore(e)

core.disable_sdk_log()



class TunnelState(Enum):
    Invalid             =  0
    Initial             =  1
    Started             =  2
    ReconnectInitiated  =  3
    Reconnecting        =  4
    Connecting          =  5
    Connected           =  6
    SessionInitiating   =  7
    SessionInitiated    =  8
    Authenticating      =  9
    Authenticated       = 10
    ForwardingInitiated = 11
    ForwardingSucceeded = 12
    Stopped             = 13
    Ended               = 14

def set_log_path(path):
    """
    Set path where native library print its log. Use this function only if requires.
    To disable native library logging completly, use `disableLog` function.

    Args:
        path (str): New log path. Path needs to have write permission.
    """
    core.pinggy_set_log_path(path)

def disable_log():
    """
    Disable logging by the native library.
    """
    core.pinggy_set_log_enable(False)

def enable_log():
    """
    Enable libpinggy log.
    """
    core.pinggy_set_log_enable(True)

setLogPath = set_log_path
disableLog = disable_log

def version():
    """
    Function to know the native library version.

    Returns:
        str: libpinggy version.
    """
    return core.pinggy_version_len()

def git_commit():
    """
    Function to get the git commit hash of the source code.

    Returns:
        str: git commit hash.
    """
    return core.pinggy_git_commit_len()

def build_timestamp():
    """
    Function to get the build timestamp as per the build-system.

    Returns:
        str: build timestamp.
    """
    return core.pinggy_build_timestamp_len()

def libc_version():
    """
    Get the libc version of the native. This information is accurate only for linux operating system.

    Returns:
        str: libc version.
    """
    return core.pinggy_libc_version_len()

def build_os():
    """
    Get the detail about the build operating system.

    Returns:
        str: os detail.
    """
    return core.pinggy_build_os_len()


class Channel:
    """
    Represents incomming channels from the tunnel.

    **This feature is not finished and not to be used**
    """
    def __init__(self, channelRef):
        self.__channelRef       = channelRef
        self.__data_received_cb = core.pinggy_channel_on_data_received_cb_t(self.__func_data_received)
        self.__ready_to_send_cb = core.pinggy_channel_on_ready_to_send_cb_t(self.__func_ready_to_send)
        self.__error_cb         = core.pinggy_channel_on_error_cb_t(self.__func_error)
        self.__cleanup_cb       = core.pinggy_channel_on_cleanup_cb_t(self.__func_cleanup)

        if not core.pinggy_tunnel_channel_set_on_data_received_callback(self.__channelRef, self.__data_received_cb, None):
            logger.error(f"Could not setup callback `pinggy_channel_data_received_cb_t` for channel {self.__channelRef}")
        if not core.pinggy_tunnel_channel_set_on_ready_to_send_callback(self.__channelRef, self.__ready_to_send_cb, None):
            logger.error(f"Could not setup callback `pinggy_channel_ready_to_send_cb_t` for channel {self.__channelRef}")
        if not core.pinggy_tunnel_channel_set_on_error_callback(self.__channelRef, self.__error_cb, None):
            logger.error(f"Could not setup callback `pinggy_channel_error_cb_t` for channel {self.__channelRef}")
        if not core.pinggy_tunnel_channel_set_on_cleanup_callback(self.__channelRef, self.__cleanup_cb, None):
            logger.error(f"Could not setup callback `pinggy_channel_cleanup_cb_t` for channel {self.__channelRef}")

    def __func_data_received(self, userdata, channelRef):
        assert channelRef == self.__channelRef
    def __func_ready_to_send(self, userdata, channelRef, bufferLen):
        assert channelRef == self.__channelRef
    def __func_error(self, userdata, channelRef, errStr, errLen):
        assert channelRef == self.__channelRef
    def __func_cleanup(self, userdata, channelRef):
        assert channelRef == self.__channelRef

    def accept(self):
        return core.pinggy_tunnel_channel_accept(self.__channelRef)
    def reject(self, val="unknown"):
        val = val if isinstance(val, bytes) else val.encode("utf-8")
        return core.pinggy_tunnel_channel_reject(self.__channelRef, val)
    def close(self):
        return core.pinggy_tunnel_channel_close(self.__channelRef)
    def send(self, data):
        assert isinstance(data, bytes)
        return core.pinggy_tunnel_channel_send(self.__channelRef, data, len(data))
    def recv(self, ln):
        buf = bytes(ln)
        return core.pinggy_tunnel_channel_recv(self.__channelRef, buf, ln)
    def have_data_to_read(self):
        return core.pinggy_tunnel_channel_have_data_to_recv(self.__channelRef)
    def have_buffer_to_write(self):
        return core.pinggy_tunnel_channel_have_buffer_to_send(self.__channelRef)
    def is_connected(self):
        return core.pinggy_tunnel_channel_is_connected(self.__channelRef)
    def get_type(self):
        return core.pinggy_tunnel_channel_get_type(self.__channelRef)
    def get_dest_port(self):
        return core.pinggy_tunnel_channel_get_dest_port(self.__channelRef)
    def get_dest_host(self):
        return core.pinggy_tunnel_channel_get_dest_host_len(self.__channelRef)
    def get_src_port(self):
        return core.pinggy_tunnel_channel_get_src_port(self.__channelRef)
    def get_src_host(self):
        return core.pinggy_tunnel_channel_get_src_host_len(self.__channelRef)

class BaseTunnelHandler:
    """
    Represent basic and default handler for :class:`Tunnel`. It provide default handler
    for various event triggered by the Tunnel. It is expected that all the event handler
    would extend this event handler.
    """
    def __init__(self, tunnel):
        """
        Initializes the basic event handler.
        Args:
            tunnel (Tunnel): The tunnel object
        """
        self.tunnel = tunnel

    def get_tunnel(self):
        """
        Returns the tunnel object
        Returns:
            Tunnel: the tunnel object
        """
        return self.tunnel

    def tunnel_established(self, url: typing.List[str]):
        """
        Triggers when pre-configured forwardings are successfully completed.
        Know more about forwarding at
        https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.

        Once this step done, one can fetch the urls from the tunnel.
        """

    def tunnel_failed(self, msg):
        """
        Triggers when pre-configured forwardings are failed. The reason is present in the msg.

        Agrs:
            msg (str): the reason why it failed.
        """
        logger.error(f"Forwarding failed with msg {msg}")

    def additional_forwarding_succeeded(self, bindAddr, forwardTo, forwardingType):
        """
        Triggers when additional forwarding completes successfully. Learn more at
        https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.

        **This is experimental and not well tested**

        Agrs:
            bindAddr (str): remote address where connection can be sent.
            forwardTo (str): address to which connection would forwarded. It is equivalen to `tcp_forward_to`.
        """
        logger.debug(f"Additional forwarding from {bindAddr} to {forwardTo} succeeded")

    def additional_forwarding_failed(self, bindAddr, forwardTo, forwardingType, err):
        """
        Triggers when additional forwarding fails
        """
        logger.error(f"Additional forwarding from {bindAddr} to {forwardTo} failed with error {err}")

    def forwardings_changed(self, forwarding):
        """
        Triggeres whenever some changes happens to the forwarding list. It basically contains list of mappings between
        public url and local forwarding. This function primarily triggers everytime some forwarding completed successfully.
        """
        pass

    def disconnected(self, msg):
        """
        Triggers when tunnel got disconnected by the server.

        Agrs:
            msg (str): disconnection reason.
        """
        logger.debug(f"Tunnel disconnected with msg {msg}")

    def tunnel_error(self, errorNo, msg, recoverable):
        """
        In case some error occures. Errors could be recoverable.

        Args:
            errorNo (int): internal error no. Currently not useful for user.
            msg (str): description
            recoverable (bool): whether a error is recoverable or not. Application should ignore recoverable errors.
        """
        logger.error(f"Tunnel error occured {errorNo}, {msg}, {recoverable}")

    def handle_channel(self):
        """
        **Do not return anything but False**
        """
        return False

    def new_channel(self, channel:Channel):
        """
        **Do not use**
        """
        logger.debug(f"New channel received. rejecting it. override `new_channel` method to handle the channel or return `False` from `handle_channel` method")
        channel.reject()

    def will_reconnect(self, messages):
        """
        Triggers when existing tunnel drops and it is configured to reconnect automatically.
        """
        pass

    def reconnecting(self, retry_cnt):
        """
        Triggers whenever sdk tries to reconnect the tunnel.
        """
        pass

    def reconnection_completed(self):
        """
        Triggers whenever new tunnel established.
        """
        logger.debug(self.tunnel.urls)
        pass

    def reconnection_failed(self, retry_cnt):
        """
        Triggers when the sdk exhaust reconnect attempt and unable to connect at all. This is an unrecoverable error.
        """
        pass

    def usage_update(self, usages):
        """
        Server provides usages update to the client. Application have to turn it on by calling `start_usage_update` function
        """
        pass

    # ------------------------------------------------------------------
    # Legacy callback stubs.
    # libpinggy 0.1.x folded these into tunnel_established/tunnel_failed
    # and no longer fires them. They exist only so legacy subclasses
    # that override them or call super().<name>() do not break.
    # ------------------------------------------------------------------
    def authenticated(self):
        pass

    def authentication_failed(self, errors):
        pass

    def primary_forwarding_succeeded(self):
        pass

    def primary_forwarding_failed(self, msg):
        pass

class Tunnel:
    """
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
    """
    def __init__(self, server_address="a.pinggy.io:443", type="", eventClass=BaseTunnelHandler):
        self.__tunnelRef                            = 0
        self.__configRef                            = 0
        self.__resumable                            = False

        self.__tunnel_established_cb                = core.pinggy_on_tunnel_established_cb_t(self.__func_tunnel_established)
        self.__tunnel_failed_cb                     = core.pinggy_on_tunnel_failed_cb_t(self.__func_tunnel_failed)
        self.__additional_forwarding_succeeded_cb   = core.pinggy_on_additional_forwarding_succeeded_cb_t(self.__func_additional_forwarding_succeeded)
        self.__additional_forwarding_failed_cb      = core.pinggy_on_additional_forwarding_failed_cb_t(self.__func_additional_forwarding_failed)
        self.__forwarding_changed_cb                = core.pinggy_on_forwardings_changed_cb_t(self.__func_forwardings_changed)
        self.__disconnected_cb                      = core.pinggy_on_disconnected_cb_t(self.__func_disconnected)
        self.__tunnel_error_cb                      = core.pinggy_on_tunnel_error_cb_t(self.__func_tunnel_error)
        self.__new_channel_cb                       = core.pinggy_on_new_channel_cb_t(self.__func_new_channel)
        self.__will_reconnect_cb                    = core.pinggy_on_will_reconnect_cb_t(self.__func_will_reconnect)
        self.__reconnecting_cb                      = core.pinggy_on_reconnecting_cb_t(self.__func_reconnecting)
        self.__reconnection_completed_cb            = core.pinggy_on_reconnection_completed_cb_t(self.__func_reconnection_completed)
        self.__reconnection_failed_cb               = core.pinggy_on_reconnection_failed_cb_t(self.__func_reconnection_failed)
        self.__usage_update_cb                      = core.pinggy_on_usage_update_cb_t(self.__func_usage_update)

        self.__configRef                            = core.pinggy_create_config()
        self.__tunnelRef                            = core.pinggy_tunnel_initiate(self.__configRef)

        self.__lock                                 = threading.Lock()
        self.__editableConfig                       = True

        self.__newForwardingMode                    = False
        self.__legacyMode                           = False
        self.__legacyTcpForwarding                  = ["tcp", "", ""]
        self.__legacyUdpForwarding                  = ["udp", "", ""]

        self.__urls                                 = []
        self.authentication_messages                = []
        self.tunnel_startup_messages                 = []
        self.server_address                         = server_address

        self.__started_event                        = threading.Event()
        self.__started_failure_msg                  = None

        self.__eventHandler                         = eventClass(self)

        self.__thread                               = None

        self.__setup_callbacks()

    def __setup_callbacks(self):
        if not core.pinggy_tunnel_set_on_tunnel_established_callback(self.__tunnelRef, self.__tunnel_established_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_on_tunnel_established_callback`")
        if not core.pinggy_tunnel_set_on_tunnel_failed_callback(self.__tunnelRef, self.__tunnel_failed_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_on_tunnel_failed_callback`")
        if not core.pinggy_tunnel_set_on_additional_forwarding_succeeded_callback(self.__tunnelRef, self.__additional_forwarding_succeeded_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_additional_forwarding_succeeded_callback`")
        if not core.pinggy_tunnel_set_on_additional_forwarding_failed_callback(self.__tunnelRef, self.__additional_forwarding_failed_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_additional_forwarding_failed_callback`")
        if not core.pinggy_tunnel_set_on_forwardings_changed_callback(self.__tunnelRef, self.__forwarding_changed_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_on_forwardings_changed_callback`")
        if not core.pinggy_tunnel_set_on_disconnected_callback(self.__tunnelRef, self.__disconnected_cb, None):
            logger.error(f"Could not setup callback for `pinggy_set_disconnected_callback`")
        if not core.pinggy_tunnel_set_on_will_reconnect_callback(self.__tunnelRef, self.__will_reconnect_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_on_will_reconnect_callback`")
        if not core.pinggy_tunnel_set_on_reconnecting_callback(self.__tunnelRef, self.__reconnecting_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_on_reconnecting_callback`")
        if not core.pinggy_tunnel_set_on_reconnection_completed_callback(self.__tunnelRef, self.__reconnection_completed_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_on_reconnection_completed_callback`")
        if not core.pinggy_tunnel_set_on_reconnection_failed_callback(self.__tunnelRef, self.__reconnection_failed_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_on_reconnection_failed_callback`")
        if not core.pinggy_tunnel_set_on_usage_update_callback(self.__tunnelRef, self.__usage_update_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_on_usage_update_callback`")
        if not core.pinggy_tunnel_set_on_tunnel_error_callback(self.__tunnelRef, self.__tunnel_error_cb, None):
            logger.error(f"Could not setup callback for `pinggy_set_tunnel_error_callback`")
        if not core.pinggy_tunnel_set_on_new_channel_callback(self.__tunnelRef, self.__new_channel_cb, None):
            logger.error(f"Could not setup callback for `pinggy_tunnel_set_new_channel_callback`")


    def __del__(self): #TODO stop tunnel if it is not already
        try:
            if self.__configRef:
                core.pinggy_free_ref(self.__configRef)
                self.__configRef = 0
            if self.__tunnelRef:
                if core.pinggy_free_ref(self.__tunnelRef) == 0:
                    logger.error("Could not free")
                self.__tunnelRef = 0
        except Exception:
            pass

    def start_with_c(self):
        """
        ** DO NOT USE THIS METHOD **
        """
        self.__editableConfig = False
        logger.warning("Kindly don't use this method")
        core.pinggy_tunnel_start(self.__tunnelRef)

    def start(self, thread=False, block_until_ready=True):
        """
        Start the tunnel with the provided configuration.

        With `thread=False` this is a blocking call that returns only when the
        tunnel stops or errors. With `thread=True` the tunnel runs in a
        background thread; by default this method still blocks until the
        tunnel has either been established (and `urls` is populated) or has
        failed to start. Pass `block_until_ready=False` to return as soon as
        the worker thread is launched.

        Args:
            thread (bool): Whether to run the tunnel in a new thread. Default is False.
            block_until_ready (bool): When `thread=True`, wait until the tunnel
                is established or fails before returning. Ignored when
                `thread=False`. Default is True.

        Raises:
            RuntimeError: If `block_until_ready=True` and the tunnel fails to
                start.
        """
        self.__editableConfig = False
        if thread:
            t = threading.Thread(target=self.__start_resume)
            self.__thread = t
            t.start()
            if block_until_ready:
                self.__wait_until_started()
        else:
            self.__start_resume()

    def __start_resume(self):
        if not self.__lock.acquire(False):
            raise Exception("Synchronization error")
        ret = core.pinggy_tunnel_start_non_blocking(self.__tunnelRef)

        while ret:
            ret = core.pinggy_tunnel_resume(self.__tunnelRef)

        self.__lock.release()
        return ret

    def connect(self):
        logger.warning("The method 'connect' has been removed and it is NO-OP now. Use start instead.")
        return True

    def stop(self):
        """Stops the running tunnel."""
        core.pinggy_tunnel_stop(self.__tunnelRef)
        if self.__thread is not None: # only if it is different thread than self.__thread
            if threading.current_thread() != self.__thread:
                self.__thread.join()
                self.__thread = None

    def wait(self):
        """Wait for tunnel to stop. It does not stop the tunnel though."""
        if self.__thread is not None and self.__thread != threading.current_thread():
            self.__thread.join()

    def __wait_until_started(self, timeout=60):
        """
        Block until the tunnel has either been established or failed.

        Args:
            timeout (float|None): Max seconds to wait. None waits forever.

        Returns:
            bool: True if the tunnel was established, False on timeout.

        Raises:
            RuntimeError: If the tunnel failed to start.
        """
        signaled = self.__started_event.wait(timeout)
        if not signaled:
            return False
        if self.__started_failure_msg is not None:
            raise RuntimeError(f"Tunnel failed to start: {self.__started_failure_msg}")
        return True

    def is_active(self):
        """Check if tunnel is active or not."""
        return core.pinggy_tunnel_is_active(self.__tunnelRef)

    def start_web_debugging(self, port=4300):
        """
        Start the web debugger. All the request would be handled internally.

        Call this function after primary forwarding completed successfully.
        """
        return core.pinggy_tunnel_start_web_debugging(self.__tunnelRef, port)

    def request_primary_forwarding(self):
        logger.warning("The method 'request_primary_forwarding' has been removed and it is NO-OP now. Use start instead.")
        return True

    def request_additional_forwarding(self, bindAddr, forwardTo, forwardingType="http"):
        """
        Once primary forwarding is done, user can request additional forwarding for other ports.

        More details at: https://pinggy.io/docs/http_tunnels/multi_port_forwarding/.
        """
        core.pinggy_tunnel_request_additional_forwarding(self.__tunnelRef, bindAddr, forwardTo, forwardingType)

    def add_callback(self, event_name, callback):
        """
        Register a function to be called for a tunnel event.

        Equivalent to setting the corresponding `on_<event_name>` property,
        but useful when the event name is only known at runtime.

        The callback is installed directly on the underlying event handler
        instance, so it overrides the matching method even when a custom
        handler class was passed via `eventClass`. The callback receives
        the same positional arguments as the corresponding `BaseTunnelHandler`
        method (no `self`).

        Args:
            event_name (str): Name of the event method to override.
            callback (callable): Function called when the event fires.

        Example:
            >>> tunnel.add_callback("tunnel_established", lambda urls: print(urls))
            >>> tunnel.on_disconnected = lambda msg: print("bye:", msg)
        """
        setattr(self.__eventHandler, event_name, callback)

    # ------------------------------------------------------------------
    # Per-event callback properties.
    #
    # Each property reads/writes the matching method on the underlying
    # event-handler instance. Setting one shadows the BaseTunnelHandler
    # default (or whatever a custom eventClass provided); reading returns
    # the currently bound function — either the user's callback or the
    # default handler method.
    # ------------------------------------------------------------------

    @property
    def on_tunnel_established(self):
        """Callback fired when forwardings are successfully established."""
        return self.__eventHandler.tunnel_established

    @on_tunnel_established.setter
    def on_tunnel_established(self, callback):
        self.__eventHandler.tunnel_established = callback

    @property
    def on_tunnel_failed(self):
        """Callback fired when forwardings could not be established."""
        return self.__eventHandler.tunnel_failed

    @on_tunnel_failed.setter
    def on_tunnel_failed(self, callback):
        self.__eventHandler.tunnel_failed = callback

    @property
    def on_additional_forwarding_succeeded(self):
        """Callback fired when an additional forwarding completes."""
        return self.__eventHandler.additional_forwarding_succeeded

    @on_additional_forwarding_succeeded.setter
    def on_additional_forwarding_succeeded(self, callback):
        self.__eventHandler.additional_forwarding_succeeded = callback

    @property
    def on_additional_forwarding_failed(self):
        """Callback fired when an additional forwarding fails."""
        return self.__eventHandler.additional_forwarding_failed

    @on_additional_forwarding_failed.setter
    def on_additional_forwarding_failed(self, callback):
        self.__eventHandler.additional_forwarding_failed = callback

    @property
    def on_forwardings_changed(self):
        """Callback fired when the forwarding list changes."""
        return self.__eventHandler.forwardings_changed

    @on_forwardings_changed.setter
    def on_forwardings_changed(self, callback):
        self.__eventHandler.forwardings_changed = callback

    @property
    def on_disconnected(self):
        """Callback fired when the tunnel is disconnected by the server."""
        return self.__eventHandler.disconnected

    @on_disconnected.setter
    def on_disconnected(self, callback):
        self.__eventHandler.disconnected = callback

    @property
    def on_tunnel_error(self):
        """Callback fired on tunnel errors (recoverable or not)."""
        return self.__eventHandler.tunnel_error

    @on_tunnel_error.setter
    def on_tunnel_error(self, callback):
        self.__eventHandler.tunnel_error = callback

    @property
    def on_will_reconnect(self):
        """Callback fired before the SDK attempts to reconnect."""
        return self.__eventHandler.will_reconnect

    @on_will_reconnect.setter
    def on_will_reconnect(self, callback):
        self.__eventHandler.will_reconnect = callback

    @property
    def on_reconnecting(self):
        """Callback fired for each reconnection attempt."""
        return self.__eventHandler.reconnecting

    @on_reconnecting.setter
    def on_reconnecting(self, callback):
        self.__eventHandler.reconnecting = callback

    @property
    def on_reconnection_completed(self):
        """Callback fired when a reconnection succeeds."""
        return self.__eventHandler.reconnection_completed

    @on_reconnection_completed.setter
    def on_reconnection_completed(self, callback):
        self.__eventHandler.reconnection_completed = callback

    @property
    def on_reconnection_failed(self):
        """Callback fired after the SDK exhausts reconnection attempts."""
        return self.__eventHandler.reconnection_failed

    @on_reconnection_failed.setter
    def on_reconnection_failed(self, callback):
        self.__eventHandler.reconnection_failed = callback

    @property
    def on_usage_update(self):
        """Callback fired when the server pushes a usage update."""
        return self.__eventHandler.usage_update

    @on_usage_update.setter
    def on_usage_update(self, callback):
        self.__eventHandler.usage_update = callback

    def start_usage_update(self):
        """
        Start usage update. It would start puching update via the callback
        """
        core.pinggy_tunnel_start_usage_update(self.__tunnelRef)

    def stop_usage_update(self):
        """
        Stop usages update.
        """
        core.pinggy_tunnel_stop_usage_update(self.__tunnelRef)

    @property
    def current_usages(self):
        """
        Get the usage.
        """
        usages = core.pinggy_tunnel_get_current_usages_len(self.__tunnelRef)
        if usages == "" or usages is None:
            return None
        return json.loads(usages)

    @property
    def greeting_msgs(self):
        """
        Get the greeting msg for the tunnel. This can be retrieved only after tunnel establishment.
        """
        msgs = core.pinggy_tunnel_get_greeting_msgs_len(self.__tunnelRef)
        if msgs == "" or msgs is None:
            return None
        return json.loads(msgs)

    @property
    def state(self) -> TunnelState:
        """
        libpinggy maintain states for each tunnels. Application can fetch these state for its own use.
        """
        c_state = core.pinggy_tunnel_get_state(self.__tunnelRef)
        return TunnelState(c_state)

    def serve_tunnel(self):
        logger.warning("The method 'serve_tunnel' has been removed and it is equivalent to `start` now. Use start instead.")
        self.start()

    # All __func_* dispatchers below receive Python-native arguments
    # (str / list[str] / int / etc.) — each cb_type built by
    # core.__make_cb_type wraps its argument-conversion into the class's
    # __new__, so `cb_type(py_func)` produces a callback whose Python
    # side already sees decoded args. No manual decoding or array
    # unpacking is needed here. Parameter names match the pinggy.h C
    # typedef for each callback.

    def __func_tunnel_established(self, user_data, tunnel_ref, urls):
        self.tunnel_startup_messages = urls
        self.__continue_polling = False
        self.__tunnel_started = True
        self.__urls = urls
        self.__started_failure_msg = None
        self.__started_event.set()
        self.__eventHandler.tunnel_established(urls)

    def __func_tunnel_failed(self, user_data, tunnel_ref, msg):
        self.tunnel_startup_messages = [msg]
        self.__continue_polling = False
        self.__started_failure_msg = msg
        self.__started_event.set()
        self.__eventHandler.tunnel_failed(msg)

    def __func_additional_forwarding_succeeded(self, user_data, tunnel_ref, bind_addr, forward_to_addr, forwarding_type):
        self.__eventHandler.additional_forwarding_succeeded(bind_addr, forward_to_addr, forwarding_type)

    def __func_additional_forwarding_failed(self, user_data, tunnel_ref, bind_addr, forward_to_addr, forwarding_type, error):
        self.__eventHandler.additional_forwarding_failed(bind_addr, forward_to_addr, forwarding_type, error)

    def __func_forwardings_changed(self, user_data, tunnel_ref, url_map):
        self.__eventHandler.forwardings_changed(url_map)

    def __func_disconnected(self, user_data, tunnel_ref, error, msg):
        self.__continue_polling = False
        self.__resumable = False
        self.__eventHandler.disconnected(error)

    def __func_tunnel_error(self, user_data, tunnel_ref, error_no, error, recoverable):
        self.__eventHandler.tunnel_error(error_no, error, recoverable)

    def __func_new_channel(self, user_data, tunnel_ref, channel_ref):
        if not self.__eventHandler.handle_channel():
            return False
        channel = Channel(channel_ref)
        self.__eventHandler.new_channel(channel)
        return True

    def __func_will_reconnect(self, user_data, tunnel_ref, error, messages):
        self.__eventHandler.will_reconnect(messages)

    def __func_reconnecting(self, user_data, tunnel_ref, retry_cnt):
        self.__eventHandler.reconnecting(retry_cnt)

    def __func_reconnection_completed(self, user_data, tunnel_ref, urls):
        self.__urls = urls
        self.__eventHandler.reconnection_completed()

    def __func_reconnection_failed(self, user_data, tunnel_ref, retry_cnt):
        self.__eventHandler.reconnection_failed(retry_cnt)

    def __func_usage_update(self, user_data, tunnel_ref, usages):
        self.__eventHandler.usage_update(json.loads(usages))


    #////////////////////
    @property
    def urls(self):
        """list(str): lists of public urls for the running tunnel (read only)"""
        return self.__urls

    @property
    def server_address(self):
        """
        str: pinggy server address. The default server address is `a.pinggy.io`. You can also add the
            port as follows: `a.pinggy.io:443`.
        """
        return core.pinggy_config_get_server_address_len(self.__configRef)

    @server_address.setter
    def server_address(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_server_address(self.__configRef, val)

    @property
    def token(self):
        """str: Token for the tunnel. One can it from `dashboard.pinggy.io`"""
        return core.pinggy_config_get_token_len(self.__configRef)

    @token.setter
    def token(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_token(self.__configRef, val)

    @property
    def forwardings(self):
        """
        Retrieves the forwarding rules (as a JSON string) from the tunnel config.
        """
        return core.pinggy_config_get_forwardings_len(self.__configRef)

    @property
    def type(self):
        return self.__legacyTcpForwarding[0]

    @type.setter
    def type(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if self.__newForwardingMode:
            raise Exception("You cannot combine lagacy mode and none legacy mode")
        self.__legacyMode = True
        self.__legacyTcpForwarding[0] = val
        self.__set_legacy_forwardings()

    @property
    def udp_type(self):
        return self.__legacyUdpForwarding[0]

    @udp_type.setter
    def udp_type(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if self.__newForwardingMode:
            raise Exception("You cannot combine lagacy mode and none legacy mode")
        self.__legacyMode = True
        self.__legacyUdpForwarding[0] = val
        self.__set_legacy_forwardings()

    @property
    def tcp_forward_to(self):
        return self.__legacyTcpForwarding[2]

    def __set_legacy_forwardings(self):
        core.pinggy_config_reset_forwardings(self.__configRef)
        if self.__legacyTcpForwarding[2] != "":
            core.pinggy_config_add_forwarding(self.__configRef, *self.__legacyTcpForwarding)
        if self.__legacyUdpForwarding[2] != "":
            core.pinggy_config_add_forwarding(self.__configRef, *self.__legacyUdpForwarding)

    @tcp_forward_to.setter
    def tcp_forward_to(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if self.__newForwardingMode:
            raise Exception("You cannot combine lagacy mode and none legacy mode")
        self.__legacyMode = True
        if type(val) == int:
            val = f"localhost:{val}"
        self.__legacyTcpForwarding[2] = val
        self.__set_legacy_forwardings()

    @property
    def udp_forward_to(self):
        return self.__legacyUdpForwarding[2]

    @udp_forward_to.setter
    def udp_forward_to(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if self.__newForwardingMode:
            raise Exception("You cannot combine lagacy mode and none legacy mode")
        self.__legacyMode = True
        if type(val) == int:
            val = f"localhost:{val}"
        self.__legacyUdpForwarding[2] = val
        self.__set_legacy_forwardings()

    @property
    def force(self):
        """bool: force flag in tunnel that terminates any existing tunnel with the same token."""
        return core.pinggy_config_get_force(self.__configRef)

    @force.setter
    def force(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_force(self.__configRef, val)

    @property
    def argument(self):
        """str: tunnel arguments for header manipulation and others."""
        return core.pinggy_config_get_argument_len(self.__configRef)

    @argument.setter
    def argument(self, val: str):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")

        if type(val) != str:
            raise Exception("Only string is allowed")

        core.pinggy_config_set_argument(self.__configRef, val)

    @property
    def advanced_parsing(self):
        """
        keep it true. Free tunnels won't work without it.
        """
        return core.pinggy_config_get_advanced_parsing(self.__configRef)

    @advanced_parsing.setter
    def advanced_parsing(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_advanced_parsing(self.__configRef, val)

    @property
    def ssl(self):
        """
        Keep it true. Production tunnel doesn't works without ssl.
        """
        return core.pinggy_config_get_ssl(self.__configRef)

    @ssl.setter
    def ssl(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_ssl(self.__configRef, val)

    @property
    def sni_server_name(self):
        """
        Do not modify unless instructed by the pinggy developers.
        """
        return core.pinggy_config_get_sni_server_name(self.__configRef)

    @sni_server_name.setter
    def sni_server_name(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_sni_server_name(self.__configRef, val)

    @property
    def insecure(self):
        """
        Keep it true. Production tunnel doesn't works without it.
        """
        return core.pinggy_config_get_insecure(self.__configRef)

    @insecure.setter
    def insecure(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_insecure(self.__configRef, val)

    @property
    def auto_reconnect(self):
        """
        Set auto_reconnecting tunnel. It is required for long running tunnel.
        """
        return core.pinggy_config_get_auto_reconnect(self.__configRef)

    @auto_reconnect.setter
    def auto_reconnect(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_auto_reconnect(self.__configRef, val)

    @property
    def max_reconnect_attempts(self):
        """
        Set number of connection attempt before it give up. Setting this to `0` means infinite attempts.
        """
        return core.pinggy_config_get_max_reconnect_attempts(self.__configRef)

    @max_reconnect_attempts.setter
    def max_reconnect_attempts(self, val):
        return core.pinggy_config_set_max_reconnect_attempts(self.__configRef, val)

    @property
    def reconnect_interval(self):
        """
        Set the interval in seconds between two reconnection attempts.
        """
        return core.pinggy_config_get_reconnect_interval(self.__configRef)

    @reconnect_interval.setter
    def reconnect_interval(self, val):
        return core.pinggy_config_set_reconnect_interval(self.__configRef, val)

    #////////////////////////////////

    @forwardings.setter
    def forwardings(self, forwardings: typing.Union[int, str, typing.List[dict]]):
        """
        Sets multiple forwarding rules for the tunnel configuration.

        This function allows you to define multiple forwarding rules either as a single
        simplified forwarding string (similar to `pinggy_config_add_forwarding_simple`)
        or as a JSON array of forwarding objects.

        If `forwardings` is a single string, it should follow the format
        `[forwarding_type://][localhost:]port`.

        If `forwardings` is a list of dictionaries, each dictionary should define a
        forwarding rule with the following properties:
        - `type`: (Optional) The type of forwarding (e.g., "http", "tcp", "udp", "tls", "tlstcp").
          Defaults to "http" if not specified.
        - `listenAddress`: (Optional) The remote address to bind to. Format: `[host][:port]`.
          An empty string or undefined means the server will assign a default binding.
          The hostname is ignored for TCP and UDP tunnels. Any schema provided will be ignored.
        - `address`: The local address to forward to. Format: `[protocol://][host]:port`.
          The `protocol` is primarily used to determine if `local_server_tls` should be
          enabled for this specific rule (e.g., `https://`). It is ignored otherwise.

        Example:
            >>> tunnel.forwardings = [{"type": "tcp", "address": "localhost:22"}] # Forwards connections to local SSH server.
            >>> tunnel.forwardings = [
            ...     {"address": "localhost:8000", "listenAddress": "your-registered-custom-domain.com"},
            ...     {"address": "localhost:4000", "listenAddress": "your-registered-subdomain.pinggy.io"}
            ... ] # Forwards requests to a custom domain to localhost:8000 and to a subdomain to localhost:4000.
        """
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if self.__legacyMode:
            raise Exception("You cannot combine lagacy mode and none legacy mode")
        self.__newForwardingMode = True
        if type(forwardings) == int:
            forwardings = "localhost:"+str(forwardings)
        if isinstance(forwardings, list):
            forwardings = json.dumps(forwardings)
        core.pinggy_config_set_forwardings(self.__configRef, forwardings)

    @forwardings.deleter
    def forwardings(self):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if self.__legacyMode:
            raise Exception("You cannot combine lagacy mode and none legacy mode")
        self.__newForwardingMode = True
        core.pinggy_config_reset_forwardings(self.__configRef)

    def add_forwarding(self, address: str, type: typing.Optional[str] = None, listen_address: typing.Optional[str] = None):
        """
        Adds a new forwarding rule to the tunnel configuration.

        This function allows you to specify how incoming connections to a remote `listen_address`
        on the Pinggy server should be forwarded to a local `address` on your local machine.

        Args:
            address (str): The local address to forward to.
                    This can be a URL (e.g., "http://localhost:3000"), an IP address
                    (e.g., "127.0.0.1:8000"), or just a port (e.g., ":5000").
                    If the schema (e.g., "http://") and host are omitted, "localhost"
                    is assumed. For example, ":3000" becomes "http://localhost:3000"
                    for HTTP forwarding.
                    If `type` is "http" and `address` specifies an "https"
                    schema (e.g., "https://localhost:443"), this implicitly enables
                    `local_server_tls` for this specific forwarding rule.

            type (str, optional): The type of forwarding.
                    Valid types are "http", "tcp", "udp", "tls", "tlstcp".
                    If an empty string or None is provided, "http" is assumed.

            listen_address (str, optional): The remote address to bind to.
                    This can be a domain name, a domain:port combination,
                    or just a port. Examples: "example.pinggy.io",
                    "example.pinggy.io:8080", ":80".
                    If empty string or None, the server will assign a default binding.
                    The hostname is ignored for TCP and UDP tunnels.
                    Any schema provided will be ignored.

        Examples:
            >>> tunnel.add_forwarding(address="localhost:8000")
        """
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if self.__legacyMode:
            raise Exception("You cannot combine lagacy mode and none legacy mode")
        self.__newForwardingMode = True
        if isinstance(address, int):
            address = f"localhost:{address}"
        if (type is None or type == "") and (listen_address is None or listen_address == ""):
            core.pinggy_config_add_forwarding_simple(self.__configRef, address)
        else:
            if listen_address is None:
                listen_address = ""
            if type is None:
                type = ""
            core.pinggy_config_add_forwarding(self.__configRef, type, listen_address, address)

    #//////////////////////

    @property
    def ipwhitelist(self):
        """list[str]|None: List of IP/IP ranges that allowed to connect to the tunnel. SDK does not verify the IP"""
        ipw = core.pinggy_config_get_ip_white_list_len(self.__configRef)
        if ipw == "" or ipw is None:
            return None
        return json.loads(ipw)

    @ipwhitelist.setter
    def ipwhitelist(self, ipwhitelist: typing.Union[typing.List[str], str]):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if type(ipwhitelist) == str:
            ipwhitelist = [ipwhitelist]
        if ipwhitelist is None:
            ipwhitelist = []
        core.pinggy_config_set_ip_white_list(self.__configRef, json.dumps(ipwhitelist))
        # self.__ipwhitelist = ipwhitelist


    @property
    def basicauth(self):
        """dict[str, str]|None: List of username and correstponding password."""
        ba = core.pinggy_config_get_basic_auths_len(self.__configRef)
        return json.loads(ba)

    @basicauth.setter
    def basicauth(self, basicauth: typing.Union[typing.List[typing.Dict[str, str]], typing.Dict[str, str]]):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if type(basicauth) == dict:
            basicauth = [{"username":u, "password": p} for u,p in basicauth.items()]
        if basicauth is None:
            basicauth = []
        core.pinggy_config_set_basic_auths(self.__configRef, json.dumps(basicauth))
        # self.__basicauth = basicauth


    @property
    def bearerauth(self):
        """list[str]|None: list of key for bearer authentication"""
        ba = core.pinggy_config_get_bearer_token_auths_len(self.__configRef)
        return json.loads(ba)

    @bearerauth.setter
    def bearerauth(self, bearerauth: typing.Union[typing.List[str], str]):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if type(bearerauth) == str:
            bearerauth = [bearerauth]
        if bearerauth is None:
            bearerauth = []
        core.pinggy_config_set_bearer_token_auths(self.__configRef, json.dumps(bearerauth))
        # self.__bearerauth = bearerauth


    def __parseHmString(self, hm: str):
        parts = hm.split(":", 1)
        if len(parts) <= 1:
            return None
        typ = parts[0]
        values = parts[1]
        if typ == "r":
            return {"type": "remove", "key": values}
        kv = hm.split(":", 1)
        if len(kv) <= 1:
            return None
        key, val = kv
        if typ == "u":
            return {"type": "update", "key": key, "value" :[val]}
        if typ == "a":
            return {"type": "add", "key": key, "value" :[val]}
        return None

    @property
    def headermodification(self):
        """list[str]|None: list of header modifications. Check https://pinggy.io/docs/advanced/live_header/ for more details"""
        ret = core.pinggy_config_get_header_manipulations_len(self.__configRef)
        return json.loads(ret)

    @headermodification.setter
    def headermodification(self, headermodifications: typing.List[typing.Dict[str, str]]):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if headermodifications is None:
            headermodifications = []
        processedHm = []
        for hm in headermodifications:
            if type(hm) != str:
                processedHm.append(hm)
                continue
            nhm = self.__parseHmString(hm)
            if nhm is not None:
                processedHm.append(nhm)
        core.pinggy_config_set_header_manipulations(self.__configRef, json.dumps(processedHm))

    def remove_header(self, header_name):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        headermod = self.headermodification
        headermod.append({"type": "remove", "key": header_name})
        self.headermodification = headermod

    def add_header(self, header_name, new_value):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")

        headermod = self.headermodification
        headermod.append({"type": "add", "key": header_name, "value": [new_value]})
        self.headermodification = headermod

    def update_header(self, header_name, new_value):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")

        headermod = self.headermodification
        headermod.append({"type": "update", "key": header_name, "value": [new_value]})
        self.headermodification = headermod

    @property
    def localservertls(self):
        """str: return current localservertls config,"""
        x = core.pinggy_config_get_local_server_tls_len(self.__configRef)
        return x

    @localservertls.setter
    def localservertls(self, val: str):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        if val is None or val == "":
            val = ""
        if type(val) != str:
            raise Exception("Only string type allowed")
        core.pinggy_config_set_local_server_tls(self.__configRef, val)


    @property
    def webdebugger_port(self):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        addr = core.pinggy_config_get_webdebugger_addr_len(self.__configRef)
        return int(addr.split(":")[1])

    @webdebugger_port.setter
    def webdebugger_port(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        return core.pinggy_config_set_webdebugger_addr(self.__configRef, "localhost:%s"%(val))


    @property
    def webdebugger_addr(self):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        return core.pinggy_config_get_webdebugger_addr_len(self.__configRef)

    @webdebugger_addr.setter
    def webdebugger_addr(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        return core.pinggy_config_set_webdebugger_addr(self.__configRef, val)


    @property
    def webdebugger(self):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        return core.pinggy_config_get_webdebugger(self.__configRef)

    @webdebugger.setter
    def webdebugger(self, val):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        return core.pinggy_config_set_webdebugger(self.__configRef, bool(val))


    @property
    def xff(self):
        """bool: whethere xff is set or not."""
        return core.pinggy_config_get_x_forwarded_for(self.__configRef)

    @xff.setter
    def xff(self, xff: bool):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_x_forwarded_for(self.__configRef, xff)


    @property
    def httpsonly(self):
        """bool: whether https only is set or not"""
        return core.pinggy_config_get_https_only(self.__configRef)

    @httpsonly.setter
    def httpsonly(self, httpsonly: bool):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_https_only(self.__configRef, httpsonly)


    @property
    def fullrequesturl(self):
        """bool: request full url. if this flag is set, full original url would be pass through `X-Pinggy-Url` header in the request"""
        return core.pinggy_config_get_original_request_url(self.__configRef)

    @fullrequesturl.setter
    def fullrequesturl(self, fullrequesturl: bool):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_original_request_url(self.__configRef, fullrequesturl)


    @property
    def allowpreflight(self):
        """bool: allow preflight requests to pass through without processing"""
        return core.pinggy_config_get_allow_preflight(self.__configRef)

    @allowpreflight.setter
    def allowpreflight(self, allowpreflight: bool):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_allow_preflight(self.__configRef, allowpreflight)


    @property
    def reverseproxy(self):
        """"bool: enables reverseproxy mode. default is true."""
        return core.pinggy_config_get_reverse_proxy(self.__configRef)

    @reverseproxy.setter
    def reverseproxy(self, reverseproxy: bool):
        if not self.__editableConfig:
            raise Exception("Tunnel is already connected, no modification allowed")
        core.pinggy_config_set_reverse_proxy(self.__configRef, reverseproxy)


def start_tunnel(
        forwardto: typing.Union[int, str] = 80,
        type: str = "http",
        token: str = "",
        force: bool = False,
        ipwhitelist: typing.Optional[typing.Union[typing.List[str], str]] = None,
        basicauth: typing.Optional[typing.Dict[str, str]] = None,
        bearerauth: typing.Optional[typing.Union[typing.List[str], str]] = None,
        headermodification: typing.Optional[typing.List[str]] = None,
        webdebuggerport: int = 0,
        xff: bool = False,
        httpsonly: bool = False,
        fullrequesturl: bool = False,
        allowpreflight: bool = False,
        reverseproxy: bool = True,
        serveraddress: str = "a.pinggy.io:443",
        udpforwardto: typing.Optional[typing.Union[int, str]] = None,
        localservertls: typing.Union[str, bool] = False,
        autoreconnect: bool = False,
        eventclass = BaseTunnelHandler
):
    """
    Start a tunnel inside a new thread and get reference to the tunnel.

    Args:
        forwardto: address of local server. Only port can be provided incase of local server. Example: 80, "localhost:80".
                    The format is [schema://][localhost:]port. Schema can be one of `http`, `https`, `tcp`, `tls`, `tlstcp`, `udp`. Default is `http`.
                    `https` means local server tls.

        type: Type of tunnel. One of `http`, `tcp`, `tls`, `tlstcp`, `udp`. Default is `http`.

        token: User token. Get it from https://dashboard.pinggy.io

        force: enable of disable force flag. Enabling it would cause to stop any existing tunnel with same token.

        ipwhitelist: list of ipaddresses that are allowed to connect to the tunnel. Example: ["2301::c4f:45c2:57e6:e637:7f1a/128","23.15.30.223/32"].
                    Be carefull about the ipv6 syntax

        basicauth: dictionary of username:password. This dictionary be used for basic authentication. Example: {"hello": "world"}

        bearerauth: list of keys that would be used for bearer key authentication. Both basicauth and bearerauth can be used together.
                    Example: ["1234"]

        headermodification: list of header modification that would be added. More detail at https://pinggy.io/docs/advanced/live_header/
                    Example: [{"type": "remove", "key": "Accept"}, {"type": "update", "key": "UserAgent", "value" :["PinggyTestServer 1.2.3"]}], ["r:Accept", "u:UserAgent:PinggyTestServer 1.2.3"]

        webdebuggerport: Webdebugging port. Webdebugging would start only if valid port is provided. Example: 4300

        localservertls: This flag enables TLS for the local server. If it is a string, it would be used as the server name for SNI. If it is True, it would be set to "localhost" by default.
                    If it is False, it would be set to None. Default: False

        xff: With this flag, pinggy adds `X-Forwarded-For` with the request header.

        httpsonly: This flag make sure that the visitor uses only the https. Any request to http would the redirected to https url.

        fullrequesturl: Pinggy server adds the original url that is requested in a header `X-Pinggy-Url ` with the request.

        allowpreflight: With this flag, pinggy detects and allow preflight request without processing so that the server can handle it.

        reverseproxy: Pinggy by default runs in reverse proxy mode. However, it can be turned off by setting this flag `False`

        serveraddress: User can set the server address to which pinggy would connect. Default: `a.pinggy.io:443`.

        udpforwardto: same as forwardto, however, it forwards a UDP destination alongside the primary forwarding.
                    Useful when one tunnel needs to expose both TCP and UDP. Use `start_udptunnel` for udp-only tunnels.

        autoreconnect: automatically reconnects when tunnel failes. It happens silently. So, to detect reconnection, one need to override the event handler.

        eventclass: event handler class. Object would be created for the tunnel.
    """

    if eventclass is None:
        eventclass = BaseTunnelHandler
    tun = Tunnel(server_address=serveraddress, eventClass=eventclass)

    tun.token                   = token
    tun.force                   = force
    try:
        tun.auto_reconnect      = autoreconnect
        #auto reconnection may not present in the library
    except:
        pass

    if bool(forwardto):
        if type in (None, "", "http"):
            tun.add_forwarding(forwardto)
        else:
            tun.add_forwarding(forwardto, type=type)

    if udpforwardto is not None:
        tun.add_forwarding(udpforwardto, type="udp")

    if ipwhitelist is not None:
        tun.ipwhitelist = ipwhitelist
    if basicauth is not None:
        tun.basicauth = basicauth
    if bearerauth is not None:
        tun.bearerauth = bearerauth
    if headermodification is not None:
        tun.headermodification = headermodification

    if isinstance(localservertls, str):
        tun.localservertls = localservertls
    elif localservertls:
        tun.localservertls = "localhost"

    tun.xff                     = xff
    tun.httpsonly               = httpsonly
    tun.fullrequesturl          = fullrequesturl
    tun.allowpreflight          = allowpreflight
    tun.reverseproxy            = reverseproxy
    tun.webdebugger_port        = webdebuggerport

    # __start_tunnel(tun, webdebuggerport)
    tun.start(True)

    return tun

def start_udptunnel(
        forwardto: typing.Union[int, str],
        token: str = "",
        force: bool = False,
        ipwhitelist: typing.Optional[typing.Union[typing.List[str], str]] = None,
        webdebuggerport: int = 4300,
        serveraddress: str = "a.pinggy.io:443",
        autoreconnect: bool = False,
        eventclass = BaseTunnelHandler
):
    """
    Start an udp tunnel inside a new thread and get reference to the tunnel.

    Args:
        forwardto: address of local server. Only port can be provided incase of local server. Example: 53, "localhost:53".

        token: User token. Get it from https://dashboard.pinggy.io

        force: enable of disable force flag. Enabling it would cause to stop any existing tunnel with same token.

        ipwhitelist: list of ipaddresses that are allowed to connect to the tunnel. Example: ["2301::c4f:45c2:57e6:e637:7f1a/128","23.15.30.223/32"].

        webdebuggerport: Webdebugging port. Webdebugging would start only if valid port is provided. Example: 4300

        serveraddress: User can set the server address to which pinggy would connect. Default: `a.pinggy.io:443`.

        autoreconnect: automatically reconnects when tunnel failes. It happens silently. So, to detect reconnection, one need to override the event handler.

        eventclass: event handler class. Object would be created for the tunnel.
    """

    if eventclass is None:
        eventclass = BaseTunnelHandler

    tun = Tunnel(server_address=serveraddress, eventClass=eventclass)

    tun.add_forwarding(forwardto, type="udp")
    tun.token                   = token
    tun.force                   = force
    try:
        tun.auto_reconnect      = autoreconnect
        #auto reconnection may not present in the library
    except:
        pass

    if ipwhitelist is not None:
        tun.ipwhitelist = ipwhitelist

    tun.webdebugger_port        = webdebuggerport

    # __start_tunnel(tun, webdebuggerport)
    tun.start(True)

    return tun


