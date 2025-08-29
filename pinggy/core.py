import ctypes
import threading
from .loader import cdll

from . import __version__ as version

pinggy_thread_local_data = threading.local()

def pinggy_error_check(a, b, c):
    err = None
    try:
        err = pinggy_thread_local_data.value
        if err is not None:
            pinggy_thread_local_data.value = None
    except Exception:
        pass

    if err is not None:
        raise Exception(err)
    return a

#========
pinggy_bool_t                                   = ctypes.c_bool
pinggy_ref_t                                    = ctypes.c_uint32
pinggy_char_p_t                                 = ctypes.c_char_p
pinggy_char_p_p_t                               = ctypes.POINTER(ctypes.c_char_p)
pinggy_void_t                                   = None
pinggy_void_p_t                                 = ctypes.c_void_p
pinggy_const_char_p_t                           = ctypes.c_char_p
pinggy_const_int_t                              = ctypes.c_int
pinggy_const_bool_t                             = ctypes.c_bool
pinggy_int_t                                    = ctypes.c_int
pinggy_len_t                                    = ctypes.c_int16
pinggy_capa_t                                   = ctypes.c_uint32
pinggy_capa_p_t                                 = ctypes.POINTER(ctypes.c_uint32)
pinggy_uint32_t                                 = ctypes.c_uint32
pinggy_uint16_t                                 = ctypes.c_uint16
pinggy_raw_len_t                                = ctypes.c_int32

pinggy_on_connected_cb_t                        = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t)
pinggy_on_authenticated_cb_t                    = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t)
pinggy_on_authentication_failed_cb_t            = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_len_t, pinggy_char_p_p_t)
pinggy_on_primary_forwarding_succeeded_cb_t     = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_len_t, pinggy_char_p_p_t)
pinggy_on_primary_forwarding_failed_cb_t        = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_const_char_p_t)
pinggy_on_additional_forwarding_succeeded_cb_t  = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_const_char_p_t, pinggy_const_char_p_t)
pinggy_on_additional_forwarding_failed_cb_t     = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_const_char_p_t, pinggy_const_char_p_t, pinggy_const_char_p_t)
pinggy_on_disconnected_cb_t                     = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_const_char_p_t, pinggy_len_t, pinggy_char_p_p_t)
pinggy_on_tunnel_error_cb_t                     = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_uint32_t, pinggy_char_p_t, pinggy_bool_t)
pinggy_on_new_channel_cb_t                      = ctypes.CFUNCTYPE(pinggy_bool_t, pinggy_void_p_t, pinggy_ref_t, pinggy_ref_t)
pinggy_on_raise_exception_cb_t                  = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_const_char_p_t, pinggy_const_char_p_t)
pinggy_on_tunnel_error_cb_t                     = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_uint32_t, pinggy_const_char_p_t, pinggy_bool_t)
pinggy_on_will_reconnect_cb_t                   = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_const_char_p_t, pinggy_len_t, pinggy_char_p_p_t)
pinggy_on_reconnecting_cb_t                     = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_uint16_t)
pinggy_on_reconnection_completed_cb_t           = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_len_t, pinggy_char_p_p_t)
pinggy_on_reconnection_failed_cb_t              = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_uint16_t)
pinggy_on_usage_update_cb_t                     = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_const_char_p_t)

pinggy_channel_data_received_cb_t               = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t)
pinggy_channel_ready_to_send_cb_t               = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_uint32_t)
pinggy_channel_error_cb_t                       = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t, pinggy_const_char_p_t, pinggy_len_t)
pinggy_channel_cleanup_cb_t                     = ctypes.CFUNCTYPE(pinggy_void_t, pinggy_void_p_t, pinggy_ref_t)

#==============================
#   Backward Compatibility
#==============================
def __fix_backward_compatibility(_cdll, _new_attr, _old_attr):
    try:
        getattr(_cdll, _new_attr)
        return
    except:
        _old_val = getattr(_cdll, _old_attr)
        setattr(_cdll, _new_attr, _old_val)

# for functions before v0.0.13
__fix_backward_compatibility(cdll, "pinggy_set_on_exception_callback",                              "pinggy_set_exception_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_connected_callback",                       "pinggy_tunnel_set_connected_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_authenticated_callback",                   "pinggy_tunnel_set_authenticated_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_authentication_failed_callback",           "pinggy_tunnel_set_authentication_failed_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_primary_forwarding_succeeded_callback",    "pinggy_tunnel_set_primary_forwarding_succeeded_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_primary_forwarding_failed_callback",       "pinggy_tunnel_set_primary_forwarding_failed_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_additional_forwarding_succeeded_callback", "pinggy_tunnel_set_additional_forwarding_succeeded_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_additional_forwarding_failed_callback",    "pinggy_tunnel_set_additional_forwarding_failed_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_disconnected_callback",                    "pinggy_tunnel_set_disconnected_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_tunnel_error_callback",                    "pinggy_tunnel_set_tunnel_error_callback")
__fix_backward_compatibility(cdll, "pinggy_tunnel_set_on_new_channel_callback",                     "pinggy_tunnel_set_new_channel_callback")


#==============================
#   Function manipulation
#==============================
class UnsupportedCallable:
    """
    A callable object that raises an exception when called.
    Useful as a placeholder for unimplemented features.
    """
    def __init__(self, operation, message=None, ret = None):
        if message is None:
            message = f"The operation `{operation}` is not supported in this version"
        self.message = message
        self.ret = ret

    def __call__(self, *args, **kwargs):
        if self.ret is not None:
            return self.ret
        raise NotImplementedError(self.message)

def __get_string_via_cfunc(func):
    def wrapper(*arg):
        buffer_size = 1024
        buffer = ctypes.create_string_buffer(buffer_size)
        len_type = False
        if func.__name__.endswith("_len"):
            len_type = True
            try:
                x = pinggy_capa_t(0)
                ln = func(*arg, buffer_size, buffer, ctypes.byref(x))
                if ln > 0 and x.value <= buffer_size:
                    res = buffer.value.decode('utf-8') if ln != 0 else ""
                buffer_size = x.value
                if buffer_size <= 0:
                    return ""
            except Exception as e:
                buffer_size = 1024
                pass
        buffer = ctypes.create_string_buffer(buffer_size)
        if len_type:
            ln = func(*arg, buffer_size, buffer, ctypes.byref(x))
        else:
            ln = func(*arg, buffer_size, buffer)
        res = buffer.value.decode('utf-8') if ln != 0 else ""
        return res
    return wrapper

def __set_string_via_cfunc(func, argtypes):
    argsToCare = []
    for i, x in enumerate(argtypes):
        if x in {pinggy_const_char_p_t, pinggy_char_p_t}:
            argsToCare.append(i)
    def wrapper(*args):
        args = list(args)
        for i in argsToCare:
            val = args[i]
            args[i] = val if isinstance(val, bytes) else val.encode("utf-8")
        return func(*args)
    if len(argsToCare):
        return wrapper
    return func


def __getFromCDLLIfSupported(funcName, restype, argtypes, getstring=False, ret=None):
    func = UnsupportedCallable(funcName, ret=ret)
    if hasattr(cdll, funcName):
        func = getattr(cdll, funcName)
    func.errcheck = pinggy_error_check
    func.argtypes = argtypes
    func.restype  = restype
    if getstring:
        func = __get_string_via_cfunc(func)
    else:
        func = __set_string_via_cfunc(func, argtypes)
    return func

def _getStringArray(l, arr):
    return [arr[i].decode('utf-8') for i in range(l)]

#==============================
pinggy_set_log_path                                             = __getFromCDLLIfSupported(
                                                                        "pinggy_set_log_path",
                                                                        pinggy_void_t,
                                                                        [pinggy_char_p_t]
                                                                        )
pinggy_set_log_enable                                           = __getFromCDLLIfSupported(
                                                                        "pinggy_set_log_enable",
                                                                        pinggy_void_t,
                                                                        [pinggy_bool_t]
                                                                        )
pinggy_set_on_exception_callback                                = __getFromCDLLIfSupported(
                                                                        "pinggy_set_on_exception_callback",
                                                                        pinggy_void_t,
                                                                        [pinggy_on_raise_exception_cb_t]
                                                                        )
pinggy_free_ref                                                 = __getFromCDLLIfSupported(
                                                                        "pinggy_free_ref",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_create_config                                            = __getFromCDLLIfSupported(
                                                                        "pinggy_create_config",
                                                                        pinggy_ref_t,
                                                                        []
                                                                        )
pinggy_config_set_server_address                                = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_server_address",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_config_set_token                                         = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_token",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_config_set_type                                          = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_type",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_config_set_udp_type                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_udp_type",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_config_set_tcp_forward_to                                = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_tcp_forward_to",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_config_set_udp_forward_to                                = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_udp_forward_to",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_config_set_force                                         = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_force",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_argument                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_argument",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_config_set_advanced_parsing                              = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_advanced_parsing",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_ssl                                           = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_ssl",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_auto_reconnect                                = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_auto_reconnect",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_sni_server_name                               = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_sni_server_name",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_config_set_insecure                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_insecure",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_header_manipulations                          = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_header_manipulations",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_const_char_p_t]
                                                                        )
pinggy_config_set_basic_auths                                   = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_basic_auths",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_const_char_p_t]
                                                                        )
pinggy_config_set_bearer_token_auths                            = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_bearer_token_auths",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_const_char_p_t]
                                                                        )
pinggy_config_set_ip_white_list                                 = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_ip_white_list",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_const_char_p_t]
                                                                        )
pinggy_config_set_reverse_proxy                                 = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_reverse_proxy",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_x_forwarder_for                               = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_x_forwarder_for",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_https_only                                    = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_https_only",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_original_request_url                          = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_original_request_url",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_allow_preflight                               = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_allow_preflight",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_no_reverse_proxy                              = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_no_reverse_proxy",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_bool_t]
                                                                        )
pinggy_config_set_local_server_tls                              = __getFromCDLLIfSupported(
                                                                        "pinggy_config_set_local_server_tls",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_const_char_p_t]
                                                                        )
pinggy_config_get_server_address                                = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_server_address",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_server_address_len                            = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_server_address_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_token                                         = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_token",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_token_len                                     = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_token_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_type                                          = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_type",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_type_len                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_type_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_udp_type                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_udp_type",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_udp_type_len                                  = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_udp_type_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_tcp_forward_to                                = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_tcp_forward_to",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_tcp_forward_to_len                            = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_tcp_forward_to_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_udp_forward_to                                = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_udp_forward_to",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_udp_forward_to_len                            = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_udp_forward_to_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_force                                         = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_force",
                                                                        pinggy_const_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_argument                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_argument",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_argument_len                                  = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_argument_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_advanced_parsing                              = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_advanced_parsing",
                                                                        pinggy_const_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_ssl                                           = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_ssl",
                                                                        pinggy_const_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_auto_reconnect                                = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_auto_reconnect",
                                                                        pinggy_const_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_sni_server_name                               = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_sni_server_name",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_sni_server_name_len                           = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_sni_server_name_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_insecure                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_insecure",
                                                                        pinggy_const_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_header_manipulations                          = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_header_manipulations",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_header_manipulations_len                      = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_header_manipulations_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_basic_auths                                   = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_basic_auths",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_basic_auths_len                               = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_basic_auths_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_bearer_token_auths                            = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_bearer_token_auths",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_bearer_token_auths_len                        = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_bearer_token_auths_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_ip_white_list                                 = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_ip_white_list",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_ip_white_list_len                             = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_ip_white_list_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_reverse_proxy                                 = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_reverse_proxy",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_x_forwarder_for                               = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_x_forwarder_for",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_https_only                                    = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_https_only",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_original_request_url                          = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_original_request_url",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_allow_preflight                               = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_allow_preflight",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_no_reverse_proxy                              = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_no_reverse_proxy",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_config_get_local_server_tls                              = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_local_server_tls",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_config_get_local_server_tls_len                          = __getFromCDLLIfSupported(
                                                                        "pinggy_config_get_local_server_tls_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_tunnel_set_on_connected_callback                         = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_connected_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_connected_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_authenticated_callback                     = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_authenticated_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_authenticated_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_authentication_failed_callback             = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_authentication_failed_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_authentication_failed_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_primary_forwarding_succeeded_callback      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_primary_forwarding_succeeded_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_primary_forwarding_succeeded_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_primary_forwarding_failed_callback         = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_primary_forwarding_failed_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_primary_forwarding_failed_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_additional_forwarding_succeeded_callback   = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_additional_forwarding_succeeded_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_additional_forwarding_succeeded_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_additional_forwarding_failed_callback      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_additional_forwarding_failed_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_additional_forwarding_failed_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_disconnected_callback                      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_disconnected_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_disconnected_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_tunnel_error_callback                      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_tunnel_error_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_tunnel_error_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_new_channel_callback                       = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_new_channel_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_new_channel_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_will_reconnect_callback                    = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_will_reconnect_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_will_reconnect_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_reconnecting_callback                      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_reconnecting_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_reconnecting_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_reconnection_completed_callback            = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_reconnection_completed_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_reconnection_completed_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_reconnection_failed_callback               = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_reconnection_failed_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_reconnection_failed_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_set_on_usage_update_callback                      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_set_on_usage_update_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_on_usage_update_cb_t, pinggy_void_p_t],
                                                                        ret=False
                                                                        )
pinggy_tunnel_initiate                                          = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_initiate",
                                                                        pinggy_ref_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_start                                             = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_start",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_connect                                           = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_connect",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_resume                                            = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_resume",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_stop                                              = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_stop",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_is_active                                         = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_is_active",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_start_web_debugging                               = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_start_web_debugging",
                                                                        pinggy_uint16_t,
                                                                        [pinggy_ref_t, pinggy_uint16_t]
                                                                        )
pinggy_tunnel_request_primary_forwarding                        = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_request_primary_forwarding",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_request_additional_forwarding                     = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_request_additional_forwarding",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t, pinggy_const_char_p_t, pinggy_const_char_p_t]
                                                                        )
pinggy_tunnel_start_usage_update                                = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_start_usage_update",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_stop_usage_update                                 = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_stop_usage_update",
                                                                        pinggy_void_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_get_current_usages                                = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_get_current_usages",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
                                                                        )
pinggy_tunnel_get_greeting_msgs                                 = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_get_greeting_msgs",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
                                                                        )
pinggy_tunnel_channel_set_data_received_callback                = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_set_data_received_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_channel_data_received_cb_t, pinggy_void_p_t]
                                                                        )
pinggy_tunnel_channel_set_ready_to_send_callback                = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_set_ready_to_send_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_channel_ready_to_send_cb_t, pinggy_void_p_t]
                                                                        )
pinggy_tunnel_channel_set_error_callback                        = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_set_error_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_channel_error_cb_t, pinggy_void_p_t]
                                                                        )
pinggy_tunnel_channel_set_cleanup_callback                      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_set_cleanup_callback",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_channel_cleanup_cb_t, pinggy_void_p_t]
                                                                        )
pinggy_tunnel_channel_accept                                    = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_accept",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_channel_reject                                    = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_reject",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t]
                                                                        )
pinggy_tunnel_channel_close                                     = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_close",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_channel_send                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_send",
                                                                        pinggy_raw_len_t,
                                                                        [pinggy_ref_t, pinggy_const_char_p_t, pinggy_raw_len_t]
                                                                        )
pinggy_tunnel_channel_recv                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_recv",
                                                                        pinggy_raw_len_t,
                                                                        [pinggy_ref_t, pinggy_char_p_t, pinggy_raw_len_t]
                                                                        )
pinggy_tunnel_channel_have_data_to_recv                         = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_have_data_to_recv",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_channel_have_buffer_to_send                       = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_have_buffer_to_send",
                                                                        pinggy_uint32_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_channel_is_connected                              = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_is_connected",
                                                                        pinggy_bool_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_channel_get_type                                  = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_get_type",
                                                                        pinggy_uint32_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_channel_get_dest_port                             = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_get_dest_port",
                                                                        pinggy_uint16_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_channel_get_dest_host                             = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_get_dest_host",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_tunnel_channel_get_dest_host_len                         = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_get_dest_host_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_tunnel_channel_get_src_port                              = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_get_src_port",
                                                                        pinggy_uint16_t,
                                                                        [pinggy_ref_t]
                                                                        )
pinggy_tunnel_channel_get_src_host                              = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_get_src_host",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_tunnel_channel_get_src_host_len                          = __getFromCDLLIfSupported(
                                                                        "pinggy_tunnel_channel_get_src_host_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_version                                                  = __getFromCDLLIfSupported(
                                                                        "pinggy_version",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_version_len                                              = __getFromCDLLIfSupported(
                                                                        "pinggy_version",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_git_commit                                               = __getFromCDLLIfSupported(
                                                                        "pinggy_git_commit",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_git_commit_len                                           = __getFromCDLLIfSupported(
                                                                        "pinggy_git_commit_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_build_timestamp                                          = __getFromCDLLIfSupported(
                                                                        "pinggy_build_timestamp",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_build_timestamp_len                                      = __getFromCDLLIfSupported(
                                                                        "pinggy_build_timestamp_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_libc_version                                             = __getFromCDLLIfSupported(
                                                                        "pinggy_libc_version",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_libc_version_len                                         = __getFromCDLLIfSupported(
                                                                        "pinggy_libc_version_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )
pinggy_build_os                                                 = __getFromCDLLIfSupported(
                                                                        "pinggy_build_os",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t],
                                                                        getstring=True
                                                                        )
pinggy_build_os_len                                             = __getFromCDLLIfSupported(
                                                                        "pinggy_build_os_len",
                                                                        pinggy_const_int_t,
                                                                        [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t],
                                                                        getstring=True
                                                                        )


#==============================
"""
pinggy_set_log_path                                             = __getFromCDLLIfSupported("pinggy_set_log_path")
pinggy_set_log_enable                                           = __getFromCDLLIfSupported("pinggy_set_log_enable")
pinggy_set_on_exception_callback                                = __getFromCDLLIfSupported("pinggy_set_on_exception_callback")
pinggy_free_ref                                                 = __getFromCDLLIfSupported("pinggy_free_ref")
pinggy_create_config                                            = __getFromCDLLIfSupported("pinggy_create_config")
pinggy_config_set_server_address                                = __getFromCDLLIfSupported("pinggy_config_set_server_address")
pinggy_config_set_token                                         = __getFromCDLLIfSupported("pinggy_config_set_token")
pinggy_config_set_type                                          = __getFromCDLLIfSupported("pinggy_config_set_type")
pinggy_config_set_udp_type                                      = __getFromCDLLIfSupported("pinggy_config_set_udp_type")
pinggy_config_set_tcp_forward_to                                = __getFromCDLLIfSupported("pinggy_config_set_tcp_forward_to")
pinggy_config_set_udp_forward_to                                = __getFromCDLLIfSupported("pinggy_config_set_udp_forward_to")
pinggy_config_set_force                                         = __getFromCDLLIfSupported("pinggy_config_set_force")
pinggy_config_set_argument                                      = __getFromCDLLIfSupported("pinggy_config_set_argument")
pinggy_config_set_advanced_parsing                              = __getFromCDLLIfSupported("pinggy_config_set_advanced_parsing")
pinggy_config_set_ssl                                           = __getFromCDLLIfSupported("pinggy_config_set_ssl")
pinggy_config_set_auto_reconnect                                = __getFromCDLLIfSupported("pinggy_config_set_auto_reconnect")
pinggy_config_set_sni_server_name                               = __getFromCDLLIfSupported("pinggy_config_set_sni_server_name")
pinggy_config_set_insecure                                      = __getFromCDLLIfSupported("pinggy_config_set_insecure")
pinggy_config_set_header_manipulations                          = __getFromCDLLIfSupported("pinggy_config_set_header_manipulations")
pinggy_config_set_basic_auths                                   = __getFromCDLLIfSupported("pinggy_config_set_basic_auths")
pinggy_config_set_bearer_token_auths                            = __getFromCDLLIfSupported("pinggy_config_set_bearer_token_auths")
pinggy_config_set_ip_white_list                                 = __getFromCDLLIfSupported("pinggy_config_set_ip_white_list")
pinggy_config_set_reverse_proxy                                 = __getFromCDLLIfSupported("pinggy_config_set_reverse_proxy")
pinggy_config_set_x_forwarder_for                               = __getFromCDLLIfSupported("pinggy_config_set_x_forwarder_for")
pinggy_config_set_https_only                                    = __getFromCDLLIfSupported("pinggy_config_set_https_only")
pinggy_config_set_original_request_url                          = __getFromCDLLIfSupported("pinggy_config_set_original_request_url")
pinggy_config_set_allow_preflight                               = __getFromCDLLIfSupported("pinggy_config_set_allow_preflight")
pinggy_config_set_no_reverse_proxy                              = __getFromCDLLIfSupported("pinggy_config_set_no_reverse_proxy")
pinggy_config_set_local_server_tls                              = __getFromCDLLIfSupported("pinggy_config_set_local_server_tls")
pinggy_config_get_server_address                                = __getFromCDLLIfSupported("pinggy_config_get_server_address")
pinggy_config_get_server_address_len                            = __getFromCDLLIfSupported("pinggy_config_get_server_address_len")
pinggy_config_get_token                                         = __getFromCDLLIfSupported("pinggy_config_get_token")
pinggy_config_get_token_len                                     = __getFromCDLLIfSupported("pinggy_config_get_token_len")
pinggy_config_get_type                                          = __getFromCDLLIfSupported("pinggy_config_get_type")
pinggy_config_get_type_len                                      = __getFromCDLLIfSupported("pinggy_config_get_type_len")
pinggy_config_get_udp_type                                      = __getFromCDLLIfSupported("pinggy_config_get_udp_type")
pinggy_config_get_udp_type_len                                  = __getFromCDLLIfSupported("pinggy_config_get_udp_type_len")
pinggy_config_get_tcp_forward_to                                = __getFromCDLLIfSupported("pinggy_config_get_tcp_forward_to")
pinggy_config_get_tcp_forward_to_len                            = __getFromCDLLIfSupported("pinggy_config_get_tcp_forward_to_len")
pinggy_config_get_udp_forward_to                                = __getFromCDLLIfSupported("pinggy_config_get_udp_forward_to")
pinggy_config_get_udp_forward_to_len                            = __getFromCDLLIfSupported("pinggy_config_get_udp_forward_to_len")
pinggy_config_get_force                                         = __getFromCDLLIfSupported("pinggy_config_get_force")
pinggy_config_get_argument                                      = __getFromCDLLIfSupported("pinggy_config_get_argument")
pinggy_config_get_argument_len                                  = __getFromCDLLIfSupported("pinggy_config_get_argument_len")
pinggy_config_get_advanced_parsing                              = __getFromCDLLIfSupported("pinggy_config_get_advanced_parsing")
pinggy_config_get_ssl                                           = __getFromCDLLIfSupported("pinggy_config_get_ssl")
pinggy_config_get_auto_reconnect                                = __getFromCDLLIfSupported("pinggy_config_get_auto_reconnect")
pinggy_config_get_sni_server_name                               = __getFromCDLLIfSupported("pinggy_config_get_sni_server_name")
pinggy_config_get_sni_server_name_len                           = __getFromCDLLIfSupported("pinggy_config_get_sni_server_name_len")
pinggy_config_get_insecure                                      = __getFromCDLLIfSupported("pinggy_config_get_insecure")
pinggy_config_get_header_manipulations                          = __getFromCDLLIfSupported("pinggy_config_get_header_manipulations")
pinggy_config_get_header_manipulations_len                      = __getFromCDLLIfSupported("pinggy_config_get_header_manipulations_len")
pinggy_config_get_basic_auths                                   = __getFromCDLLIfSupported("pinggy_config_get_basic_auths")
pinggy_config_get_basic_auths_len                               = __getFromCDLLIfSupported("pinggy_config_get_basic_auths_len")
pinggy_config_get_bearer_token_auths                            = __getFromCDLLIfSupported("pinggy_config_get_bearer_token_auths")
pinggy_config_get_bearer_token_auths_len                        = __getFromCDLLIfSupported("pinggy_config_get_bearer_token_auths_len")
pinggy_config_get_ip_white_list                                 = __getFromCDLLIfSupported("pinggy_config_get_ip_white_list")
pinggy_config_get_ip_white_list_len                             = __getFromCDLLIfSupported("pinggy_config_get_ip_white_list_len")
pinggy_config_get_reverse_proxy                                 = __getFromCDLLIfSupported("pinggy_config_get_reverse_proxy")
pinggy_config_get_x_forwarder_for                               = __getFromCDLLIfSupported("pinggy_config_get_x_forwarder_for")
pinggy_config_get_https_only                                    = __getFromCDLLIfSupported("pinggy_config_get_https_only")
pinggy_config_get_original_request_url                          = __getFromCDLLIfSupported("pinggy_config_get_original_request_url")
pinggy_config_get_allow_preflight                               = __getFromCDLLIfSupported("pinggy_config_get_allow_preflight")
pinggy_config_get_no_reverse_proxy                              = __getFromCDLLIfSupported("pinggy_config_get_no_reverse_proxy")
pinggy_config_get_local_server_tls                              = __getFromCDLLIfSupported("pinggy_config_get_local_server_tls")
pinggy_config_get_local_server_tls_len                          = __getFromCDLLIfSupported("pinggy_config_get_local_server_tls_len")
pinggy_tunnel_set_on_connected_callback                         = __getFromCDLLIfSupported("pinggy_tunnel_set_on_connected_callback", ret=False)
pinggy_tunnel_set_on_authenticated_callback                     = __getFromCDLLIfSupported("pinggy_tunnel_set_on_authenticated_callback", ret=False)
pinggy_tunnel_set_on_authentication_failed_callback             = __getFromCDLLIfSupported("pinggy_tunnel_set_on_authentication_failed_callback", ret=False)
pinggy_tunnel_set_on_primary_forwarding_succeeded_callback      = __getFromCDLLIfSupported("pinggy_tunnel_set_on_primary_forwarding_succeeded_callback", ret=False)
pinggy_tunnel_set_on_primary_forwarding_failed_callback         = __getFromCDLLIfSupported("pinggy_tunnel_set_on_primary_forwarding_failed_callback", ret=False)
pinggy_tunnel_set_on_additional_forwarding_succeeded_callback   = __getFromCDLLIfSupported("pinggy_tunnel_set_on_additional_forwarding_succeeded_callback", ret=False)
pinggy_tunnel_set_on_additional_forwarding_failed_callback      = __getFromCDLLIfSupported("pinggy_tunnel_set_on_additional_forwarding_failed_callback", ret=False)
pinggy_tunnel_set_on_disconnected_callback                      = __getFromCDLLIfSupported("pinggy_tunnel_set_on_disconnected_callback", ret=False)
pinggy_tunnel_set_on_tunnel_error_callback                      = __getFromCDLLIfSupported("pinggy_tunnel_set_on_tunnel_error_callback", ret=False)
pinggy_tunnel_set_on_new_channel_callback                       = __getFromCDLLIfSupported("pinggy_tunnel_set_on_new_channel_callback", ret=False)
pinggy_tunnel_set_on_will_reconnect_callback                    = __getFromCDLLIfSupported("pinggy_tunnel_set_on_will_reconnect_callback", ret=False)
pinggy_tunnel_set_on_reconnecting_callback                      = __getFromCDLLIfSupported("pinggy_tunnel_set_on_reconnecting_callback", ret=False)
pinggy_tunnel_set_on_reconnection_completed_callback            = __getFromCDLLIfSupported("pinggy_tunnel_set_on_reconnection_completed_callback", ret=False)
pinggy_tunnel_set_on_reconnection_failed_callback               = __getFromCDLLIfSupported("pinggy_tunnel_set_on_reconnection_failed_callback", ret=False)
pinggy_tunnel_set_on_usage_update_callback                      = __getFromCDLLIfSupported("pinggy_tunnel_set_on_usage_update_callback", ret=False)
pinggy_tunnel_initiate                                          = __getFromCDLLIfSupported("pinggy_tunnel_initiate")
pinggy_tunnel_start                                             = __getFromCDLLIfSupported("pinggy_tunnel_start")
pinggy_tunnel_connect                                           = __getFromCDLLIfSupported("pinggy_tunnel_connect")
pinggy_tunnel_resume                                            = __getFromCDLLIfSupported("pinggy_tunnel_resume")
pinggy_tunnel_stop                                              = __getFromCDLLIfSupported("pinggy_tunnel_stop")
pinggy_tunnel_is_active                                         = __getFromCDLLIfSupported("pinggy_tunnel_is_active")
pinggy_tunnel_start_web_debugging                               = __getFromCDLLIfSupported("pinggy_tunnel_start_web_debugging")
pinggy_tunnel_request_primary_forwarding                        = __getFromCDLLIfSupported("pinggy_tunnel_request_primary_forwarding")
pinggy_tunnel_request_additional_forwarding                     = __getFromCDLLIfSupported("pinggy_tunnel_request_additional_forwarding")
pinggy_tunnel_start_usage_update                                = __getFromCDLLIfSupported("pinggy_tunnel_start_usage_update")
pinggy_tunnel_stop_usage_update                                 = __getFromCDLLIfSupported("pinggy_tunnel_stop_usage_update")
pinggy_tunnel_get_current_usages                                = __getFromCDLLIfSupported("pinggy_tunnel_get_current_usages")
pinggy_tunnel_get_greeting_msgs                                 = __getFromCDLLIfSupported("pinggy_tunnel_get_greeting_msgs")
#==============

pinggy_tunnel_channel_set_data_received_callback                = __getFromCDLLIfSupported("pinggy_tunnel_channel_set_data_received_callback")
pinggy_tunnel_channel_set_ready_to_send_callback                = __getFromCDLLIfSupported("pinggy_tunnel_channel_set_ready_to_send_callback")
pinggy_tunnel_channel_set_error_callback                        = __getFromCDLLIfSupported("pinggy_tunnel_channel_set_error_callback")
pinggy_tunnel_channel_set_cleanup_callback                      = __getFromCDLLIfSupported("pinggy_tunnel_channel_set_cleanup_callback")
pinggy_tunnel_channel_accept                                    = __getFromCDLLIfSupported("pinggy_tunnel_channel_accept")
pinggy_tunnel_channel_reject                                    = __getFromCDLLIfSupported("pinggy_tunnel_channel_reject")
pinggy_tunnel_channel_close                                     = __getFromCDLLIfSupported("pinggy_tunnel_channel_close")
pinggy_tunnel_channel_send                                      = __getFromCDLLIfSupported("pinggy_tunnel_channel_send")
pinggy_tunnel_channel_recv                                      = __getFromCDLLIfSupported("pinggy_tunnel_channel_recv")
pinggy_tunnel_channel_have_data_to_recv                         = __getFromCDLLIfSupported("pinggy_tunnel_channel_have_data_to_recv")
pinggy_tunnel_channel_have_buffer_to_send                       = __getFromCDLLIfSupported("pinggy_tunnel_channel_have_buffer_to_send")
pinggy_tunnel_channel_is_connected                              = __getFromCDLLIfSupported("pinggy_tunnel_channel_is_connected")
pinggy_tunnel_channel_get_type                                  = __getFromCDLLIfSupported("pinggy_tunnel_channel_get_type")
pinggy_tunnel_channel_get_dest_port                             = __getFromCDLLIfSupported("pinggy_tunnel_channel_get_dest_port")
pinggy_tunnel_channel_get_dest_host                             = __getFromCDLLIfSupported("pinggy_tunnel_channel_get_dest_host")
pinggy_tunnel_channel_get_dest_host_len                         = __getFromCDLLIfSupported("pinggy_tunnel_channel_get_dest_host_len")
pinggy_tunnel_channel_get_src_port                              = __getFromCDLLIfSupported("pinggy_tunnel_channel_get_src_port")
pinggy_tunnel_channel_get_src_host                              = __getFromCDLLIfSupported("pinggy_tunnel_channel_get_src_host")
pinggy_tunnel_channel_get_src_host_len                          = __getFromCDLLIfSupported("pinggy_tunnel_channel_get_src_host_len")
pinggy_version                                                  = __getFromCDLLIfSupported("pinggy_version")
pinggy_version_len                                              = __getFromCDLLIfSupported("pinggy_version")
pinggy_git_commit                                               = __getFromCDLLIfSupported("pinggy_git_commit")
pinggy_git_commit_len                                           = __getFromCDLLIfSupported("pinggy_git_commit_len")
pinggy_build_timestamp                                          = __getFromCDLLIfSupported("pinggy_build_timestamp")
pinggy_build_timestamp_len                                      = __getFromCDLLIfSupported("pinggy_build_timestamp_len")
pinggy_libc_version                                             = __getFromCDLLIfSupported("pinggy_libc_version")
pinggy_libc_version_len                                         = __getFromCDLLIfSupported("pinggy_libc_version_len")
pinggy_build_os                                                 = __getFromCDLLIfSupported("pinggy_build_os")
pinggy_build_os_len                                             = __getFromCDLLIfSupported("pinggy_build_os_len")


#==========
pinggy_set_log_path.errcheck                                            = pinggy_error_check
pinggy_set_log_enable.errcheck                                          = pinggy_error_check
pinggy_set_on_exception_callback.errcheck                               = pinggy_error_check
pinggy_free_ref.errcheck                                                = pinggy_error_check
pinggy_create_config.errcheck                                           = pinggy_error_check
pinggy_config_set_server_address.errcheck                               = pinggy_error_check
pinggy_config_set_token.errcheck                                        = pinggy_error_check
pinggy_config_set_type.errcheck                                         = pinggy_error_check
pinggy_config_set_udp_type.errcheck                                     = pinggy_error_check
pinggy_config_set_tcp_forward_to.errcheck                               = pinggy_error_check
pinggy_config_set_udp_forward_to.errcheck                               = pinggy_error_check
pinggy_config_set_force.errcheck                                        = pinggy_error_check
pinggy_config_set_argument.errcheck                                     = pinggy_error_check
pinggy_config_set_advanced_parsing.errcheck                             = pinggy_error_check
pinggy_config_set_ssl.errcheck                                          = pinggy_error_check
pinggy_config_set_auto_reconnect.errcheck                               = pinggy_error_check
pinggy_config_set_sni_server_name.errcheck                              = pinggy_error_check
pinggy_config_set_insecure.errcheck                                     = pinggy_error_check
pinggy_config_set_header_manipulations.errcheck                         = pinggy_error_check
pinggy_config_set_basic_auths.errcheck                                  = pinggy_error_check
pinggy_config_set_bearer_token_auths.errcheck                           = pinggy_error_check
pinggy_config_set_ip_white_list.errcheck                                = pinggy_error_check
pinggy_config_set_reverse_proxy.errcheck                                = pinggy_error_check
pinggy_config_set_x_forwarder_for.errcheck                              = pinggy_error_check
pinggy_config_set_https_only.errcheck                                   = pinggy_error_check
pinggy_config_set_original_request_url.errcheck                         = pinggy_error_check
pinggy_config_set_allow_preflight.errcheck                              = pinggy_error_check
pinggy_config_set_no_reverse_proxy.errcheck                             = pinggy_error_check
pinggy_config_set_local_server_tls.errcheck                             = pinggy_error_check
pinggy_config_get_server_address.errcheck                               = pinggy_error_check
pinggy_config_get_server_address_len.errcheck                           = pinggy_error_check
pinggy_config_get_token.errcheck                                        = pinggy_error_check
pinggy_config_get_token_len.errcheck                                    = pinggy_error_check
pinggy_config_get_type.errcheck                                         = pinggy_error_check
pinggy_config_get_type_len.errcheck                                     = pinggy_error_check
pinggy_config_get_udp_type.errcheck                                     = pinggy_error_check
pinggy_config_get_udp_type_len.errcheck                                 = pinggy_error_check
pinggy_config_get_tcp_forward_to.errcheck                               = pinggy_error_check
pinggy_config_get_tcp_forward_to_len.errcheck                           = pinggy_error_check
pinggy_config_get_udp_forward_to.errcheck                               = pinggy_error_check
pinggy_config_get_udp_forward_to_len.errcheck                           = pinggy_error_check
pinggy_config_get_force.errcheck                                        = pinggy_error_check
pinggy_config_get_argument.errcheck                                     = pinggy_error_check
pinggy_config_get_argument_len.errcheck                                 = pinggy_error_check
pinggy_config_get_advanced_parsing.errcheck                             = pinggy_error_check
pinggy_config_get_ssl.errcheck                                          = pinggy_error_check
pinggy_config_get_auto_reconnect.errcheck                               = pinggy_error_check
pinggy_config_get_sni_server_name.errcheck                              = pinggy_error_check
pinggy_config_get_sni_server_name_len.errcheck                          = pinggy_error_check
pinggy_config_get_insecure.errcheck                                     = pinggy_error_check
pinggy_config_get_header_manipulations.errcheck                         = pinggy_error_check
pinggy_config_get_header_manipulations_len.errcheck                     = pinggy_error_check
pinggy_config_get_basic_auths.errcheck                                  = pinggy_error_check
pinggy_config_get_basic_auths_len.errcheck                              = pinggy_error_check
pinggy_config_get_bearer_token_auths.errcheck                           = pinggy_error_check
pinggy_config_get_bearer_token_auths_len.errcheck                       = pinggy_error_check
pinggy_config_get_ip_white_list.errcheck                                = pinggy_error_check
pinggy_config_get_ip_white_list_len.errcheck                            = pinggy_error_check
pinggy_config_get_reverse_proxy.errcheck                                = pinggy_error_check
pinggy_config_get_x_forwarder_for.errcheck                              = pinggy_error_check
pinggy_config_get_https_only.errcheck                                   = pinggy_error_check
pinggy_config_get_original_request_url.errcheck                         = pinggy_error_check
pinggy_config_get_allow_preflight.errcheck                              = pinggy_error_check
pinggy_config_get_no_reverse_proxy.errcheck                             = pinggy_error_check
pinggy_config_get_local_server_tls.errcheck                             = pinggy_error_check
pinggy_config_get_local_server_tls_len.errcheck                         = pinggy_error_check
pinggy_tunnel_set_on_connected_callback.errcheck                        = pinggy_error_check
pinggy_tunnel_set_on_authenticated_callback.errcheck                    = pinggy_error_check
pinggy_tunnel_set_on_authentication_failed_callback.errcheck            = pinggy_error_check
pinggy_tunnel_set_on_primary_forwarding_succeeded_callback.errcheck     = pinggy_error_check
pinggy_tunnel_set_on_primary_forwarding_failed_callback.errcheck        = pinggy_error_check
pinggy_tunnel_set_on_additional_forwarding_succeeded_callback.errcheck  = pinggy_error_check
pinggy_tunnel_set_on_additional_forwarding_failed_callback.errcheck     = pinggy_error_check
pinggy_tunnel_set_on_disconnected_callback.errcheck                     = pinggy_error_check
pinggy_tunnel_set_on_tunnel_error_callback.errcheck                     = pinggy_error_check
pinggy_tunnel_set_on_new_channel_callback.errcheck                      = pinggy_error_check
pinggy_tunnel_set_on_will_reconnect_callback.errcheck                   = pinggy_error_check
pinggy_tunnel_set_on_reconnecting_callback.errcheck                     = pinggy_error_check
pinggy_tunnel_set_on_reconnection_completed_callback.errcheck           = pinggy_error_check
pinggy_tunnel_set_on_reconnection_failed_callback.errcheck              = pinggy_error_check
pinggy_tunnel_set_on_usage_update_callback.errcheck                     = pinggy_error_check
pinggy_tunnel_initiate.errcheck                                         = pinggy_error_check
pinggy_tunnel_start.errcheck                                            = pinggy_error_check
pinggy_tunnel_connect.errcheck                                          = pinggy_error_check
pinggy_tunnel_resume.errcheck                                           = pinggy_error_check
pinggy_tunnel_stop.errcheck                                             = pinggy_error_check
pinggy_tunnel_is_active.errcheck                                        = pinggy_error_check
pinggy_tunnel_start_web_debugging.errcheck                              = pinggy_error_check
pinggy_tunnel_request_primary_forwarding.errcheck                       = pinggy_error_check
pinggy_tunnel_request_additional_forwarding.errcheck                    = pinggy_error_check
pinggy_tunnel_start_usage_update.errcheck                               = pinggy_error_check
pinggy_tunnel_stop_usage_update.errcheck                                = pinggy_error_check
pinggy_tunnel_get_current_usages.errcheck                               = pinggy_error_check
pinggy_tunnel_get_greeting_msgs.errcheck                                = pinggy_error_check
#========
pinggy_set_log_path.restype                                             = pinggy_void_t
pinggy_set_log_enable.restype                                           = pinggy_void_t
pinggy_set_on_exception_callback.restype                                = pinggy_void_t
pinggy_free_ref.restype                                                 = pinggy_bool_t
pinggy_create_config.restype                                            = pinggy_ref_t
pinggy_config_set_server_address.restype                                = pinggy_void_t
pinggy_config_set_token.restype                                         = pinggy_void_t
pinggy_config_set_type.restype                                          = pinggy_void_t
pinggy_config_set_udp_type.restype                                      = pinggy_void_t
pinggy_config_set_tcp_forward_to.restype                                = pinggy_void_t
pinggy_config_set_udp_forward_to.restype                                = pinggy_void_t
pinggy_config_set_force.restype                                         = pinggy_void_t
pinggy_config_set_argument.restype                                      = pinggy_void_t
pinggy_config_set_advanced_parsing.restype                              = pinggy_void_t
pinggy_config_set_ssl.restype                                           = pinggy_void_t
pinggy_config_set_auto_reconnect.restype                                = pinggy_void_t
pinggy_config_set_sni_server_name.restype                               = pinggy_void_t
pinggy_config_set_insecure.restype                                      = pinggy_void_t
pinggy_config_set_header_manipulations.restype                          = pinggy_void_t
pinggy_config_set_basic_auths.restype                                   = pinggy_void_t
pinggy_config_set_bearer_token_auths.restype                            = pinggy_void_t
pinggy_config_set_ip_white_list.restype                                 = pinggy_void_t
pinggy_config_set_reverse_proxy.restype                                 = pinggy_void_t
pinggy_config_set_x_forwarder_for.restype                               = pinggy_void_t
pinggy_config_set_https_only.restype                                    = pinggy_void_t
pinggy_config_set_original_request_url.restype                          = pinggy_void_t
pinggy_config_set_allow_preflight.restype                               = pinggy_void_t
pinggy_config_set_no_reverse_proxy.restype                              = pinggy_void_t
pinggy_config_set_local_server_tls.restype                              = pinggy_void_t
pinggy_config_get_server_address.restype                                = pinggy_const_int_t
pinggy_config_get_server_address_len.restype                            = pinggy_const_int_t
pinggy_config_get_token.restype                                         = pinggy_const_int_t
pinggy_config_get_token_len.restype                                     = pinggy_const_int_t
pinggy_config_get_type.restype                                          = pinggy_const_int_t
pinggy_config_get_type_len.restype                                      = pinggy_const_int_t
pinggy_config_get_udp_type.restype                                      = pinggy_const_int_t
pinggy_config_get_udp_type_len.restype                                  = pinggy_const_int_t
pinggy_config_get_tcp_forward_to.restype                                = pinggy_const_int_t
pinggy_config_get_tcp_forward_to_len.restype                            = pinggy_const_int_t
pinggy_config_get_udp_forward_to.restype                                = pinggy_const_int_t
pinggy_config_get_udp_forward_to_len.restype                            = pinggy_const_int_t
pinggy_config_get_force.restype                                         = pinggy_const_bool_t
pinggy_config_get_argument.restype                                      = pinggy_const_int_t
pinggy_config_get_argument_len.restype                                  = pinggy_const_int_t
pinggy_config_get_advanced_parsing.restype                              = pinggy_const_bool_t
pinggy_config_get_ssl.restype                                           = pinggy_const_bool_t
pinggy_config_get_auto_reconnect.restype                                = pinggy_const_bool_t
pinggy_config_get_sni_server_name.restype                               = pinggy_const_int_t
pinggy_config_get_sni_server_name_len.restype                           = pinggy_const_int_t
pinggy_config_get_insecure.restype                                      = pinggy_const_bool_t
pinggy_config_get_header_manipulations.restype                          = pinggy_const_int_t
pinggy_config_get_header_manipulations_len.restype                      = pinggy_const_int_t
pinggy_config_get_basic_auths.restype                                   = pinggy_const_int_t
pinggy_config_get_basic_auths_len.restype                               = pinggy_const_int_t
pinggy_config_get_bearer_token_auths.restype                            = pinggy_const_int_t
pinggy_config_get_bearer_token_auths_len.restype                        = pinggy_const_int_t
pinggy_config_get_ip_white_list.restype                                 = pinggy_const_int_t
pinggy_config_get_ip_white_list_len.restype                             = pinggy_const_int_t
pinggy_config_get_reverse_proxy.restype                                 = pinggy_bool_t
pinggy_config_get_x_forwarder_for.restype                               = pinggy_bool_t
pinggy_config_get_https_only.restype                                    = pinggy_bool_t
pinggy_config_get_original_request_url.restype                          = pinggy_bool_t
pinggy_config_get_allow_preflight.restype                               = pinggy_bool_t
pinggy_config_get_no_reverse_proxy.restype                              = pinggy_bool_t
pinggy_config_get_local_server_tls.restype                              = pinggy_const_int_t
pinggy_config_get_local_server_tls_len.restype                          = pinggy_const_int_t
pinggy_tunnel_set_on_connected_callback.restype                         = pinggy_bool_t
pinggy_tunnel_set_on_authenticated_callback.restype                     = pinggy_bool_t
pinggy_tunnel_set_on_authentication_failed_callback.restype             = pinggy_bool_t
pinggy_tunnel_set_on_primary_forwarding_succeeded_callback.restype      = pinggy_bool_t
pinggy_tunnel_set_on_primary_forwarding_failed_callback.restype         = pinggy_bool_t
pinggy_tunnel_set_on_additional_forwarding_succeeded_callback.restype   = pinggy_bool_t
pinggy_tunnel_set_on_additional_forwarding_failed_callback.restype      = pinggy_bool_t
pinggy_tunnel_set_on_disconnected_callback.restype                      = pinggy_bool_t
pinggy_tunnel_set_on_tunnel_error_callback.restype                      = pinggy_bool_t
pinggy_tunnel_set_on_new_channel_callback.restype                       = pinggy_bool_t
pinggy_tunnel_set_on_will_reconnect_callback.restype                    = pinggy_bool_t
pinggy_tunnel_set_on_reconnecting_callback.restype                      = pinggy_bool_t
pinggy_tunnel_set_on_reconnection_completed_callback.restype            = pinggy_bool_t
pinggy_tunnel_set_on_reconnection_failed_callback.restype               = pinggy_bool_t
pinggy_tunnel_set_on_usage_update_callback.restype                      = pinggy_bool_t
pinggy_tunnel_initiate.restype                                          = pinggy_ref_t
pinggy_tunnel_start.restype                                             = pinggy_bool_t
pinggy_tunnel_connect.restype                                           = pinggy_bool_t
pinggy_tunnel_resume.restype                                            = pinggy_bool_t
pinggy_tunnel_stop.restype                                              = pinggy_bool_t
pinggy_tunnel_is_active.restype                                         = pinggy_bool_t
pinggy_tunnel_start_web_debugging.restype                               = pinggy_uint16_t
pinggy_tunnel_request_primary_forwarding.restype                        = pinggy_void_t
pinggy_tunnel_request_additional_forwarding.restype                     = pinggy_void_t
pinggy_tunnel_start_usage_update.restype                                = pinggy_void_t
pinggy_tunnel_stop_usage_update.restype                                 = pinggy_void_t
pinggy_tunnel_get_current_usages.restype                                = pinggy_const_int_t
pinggy_tunnel_get_greeting_msgs.restype                                 = pinggy_const_int_t
#========
pinggy_set_log_path.argtypes                                            = [pinggy_char_p_t]
pinggy_set_log_enable.argtypes                                          = [pinggy_bool_t]
pinggy_set_on_exception_callback.argtypes                               = [pinggy_on_raise_exception_cb_t]
pinggy_free_ref.argtypes                                                = [pinggy_ref_t]
pinggy_create_config.argtypes                                           = []
pinggy_config_set_server_address.argtypes                               = [pinggy_ref_t, pinggy_char_p_t]
pinggy_config_set_token.argtypes                                        = [pinggy_ref_t, pinggy_char_p_t]
pinggy_config_set_type.argtypes                                         = [pinggy_ref_t, pinggy_char_p_t]
pinggy_config_set_udp_type.argtypes                                     = [pinggy_ref_t, pinggy_char_p_t]
pinggy_config_set_tcp_forward_to.argtypes                               = [pinggy_ref_t, pinggy_char_p_t]
pinggy_config_set_udp_forward_to.argtypes                               = [pinggy_ref_t, pinggy_char_p_t]
pinggy_config_set_force.argtypes                                        = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_argument.argtypes                                     = [pinggy_ref_t, pinggy_char_p_t]
pinggy_config_set_advanced_parsing.argtypes                             = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_ssl.argtypes                                          = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_auto_reconnect.argtypes                               = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_sni_server_name.argtypes                              = [pinggy_ref_t, pinggy_char_p_t]
pinggy_config_set_insecure.argtypes                                     = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_header_manipulations.argtypes                         = [pinggy_ref_t, pinggy_const_char_p_t]
pinggy_config_set_basic_auths.argtypes                                  = [pinggy_ref_t, pinggy_const_char_p_t]
pinggy_config_set_bearer_token_auths.argtypes                           = [pinggy_ref_t, pinggy_const_char_p_t]
pinggy_config_set_ip_white_list.argtypes                                = [pinggy_ref_t, pinggy_const_char_p_t]
pinggy_config_set_reverse_proxy.argtypes                                = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_x_forwarder_for.argtypes                              = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_https_only.argtypes                                   = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_original_request_url.argtypes                         = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_allow_preflight.argtypes                              = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_no_reverse_proxy.argtypes                             = [pinggy_ref_t, pinggy_bool_t]
pinggy_config_set_local_server_tls.argtypes                             = [pinggy_ref_t, pinggy_const_char_p_t]
pinggy_config_get_server_address.argtypes                               = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_server_address_len.argtypes                           = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_token.argtypes                                        = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_token_len.argtypes                                    = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_type.argtypes                                         = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_type_len.argtypes                                     = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_udp_type.argtypes                                     = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_udp_type_len.argtypes                                 = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_tcp_forward_to.argtypes                               = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_tcp_forward_to_len.argtypes                           = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_udp_forward_to.argtypes                               = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_udp_forward_to_len.argtypes                           = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_force.argtypes                                        = [pinggy_ref_t]
pinggy_config_get_argument.argtypes                                     = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_argument_len.argtypes                                 = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_advanced_parsing.argtypes                             = [pinggy_ref_t]
pinggy_config_get_ssl.argtypes                                          = [pinggy_ref_t]
pinggy_config_get_auto_reconnect.argtypes                               = [pinggy_ref_t]
pinggy_config_get_sni_server_name.argtypes                              = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_sni_server_name_len.argtypes                          = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_insecure.argtypes                                     = [pinggy_ref_t]
pinggy_config_get_header_manipulations.argtypes                         = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_header_manipulations_len.argtypes                     = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_basic_auths.argtypes                                  = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_basic_auths_len.argtypes                              = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_bearer_token_auths.argtypes                           = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_bearer_token_auths_len.argtypes                       = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_ip_white_list.argtypes                                = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_ip_white_list_len.argtypes                            = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_config_get_reverse_proxy.argtypes                                = [pinggy_ref_t]
pinggy_config_get_x_forwarder_for.argtypes                              = [pinggy_ref_t]
pinggy_config_get_https_only.argtypes                                   = [pinggy_ref_t]
pinggy_config_get_original_request_url.argtypes                         = [pinggy_ref_t]
pinggy_config_get_allow_preflight.argtypes                              = [pinggy_ref_t]
pinggy_config_get_no_reverse_proxy.argtypes                             = [pinggy_ref_t]
pinggy_config_get_local_server_tls.argtypes                             = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_config_get_local_server_tls_len.argtypes                         = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_tunnel_set_on_connected_callback.argtypes                        = [pinggy_ref_t, pinggy_on_connected_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_authenticated_callback.argtypes                    = [pinggy_ref_t, pinggy_on_authenticated_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_authentication_failed_callback.argtypes            = [pinggy_ref_t, pinggy_on_authentication_failed_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_primary_forwarding_succeeded_callback.argtypes     = [pinggy_ref_t, pinggy_on_primary_forwarding_succeeded_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_primary_forwarding_failed_callback.argtypes        = [pinggy_ref_t, pinggy_on_primary_forwarding_failed_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_additional_forwarding_succeeded_callback.argtypes  = [pinggy_ref_t, pinggy_on_additional_forwarding_succeeded_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_additional_forwarding_failed_callback.argtypes     = [pinggy_ref_t, pinggy_on_additional_forwarding_failed_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_disconnected_callback.argtypes                     = [pinggy_ref_t, pinggy_on_disconnected_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_tunnel_error_callback.argtypes                     = [pinggy_ref_t, pinggy_on_tunnel_error_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_new_channel_callback.argtypes                      = [pinggy_ref_t, pinggy_on_new_channel_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_will_reconnect_callback.argtypes                   = [pinggy_ref_t, pinggy_on_will_reconnect_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_reconnecting_callback.argtypes                     = [pinggy_ref_t, pinggy_on_reconnecting_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_reconnection_completed_callback.argtypes           = [pinggy_ref_t, pinggy_on_reconnection_completed_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_reconnection_failed_callback.argtypes              = [pinggy_ref_t, pinggy_on_reconnection_failed_cb_t, pinggy_void_p_t]
pinggy_tunnel_set_on_usage_update_callback.argtypes                     = [pinggy_ref_t, pinggy_on_usage_update_cb_t, pinggy_void_p_t]
pinggy_tunnel_initiate.argtypes                                         = [pinggy_ref_t]
pinggy_tunnel_start.argtypes                                            = [pinggy_ref_t]
pinggy_tunnel_connect.argtypes                                          = [pinggy_ref_t]
pinggy_tunnel_resume.argtypes                                           = [pinggy_ref_t]
pinggy_tunnel_stop.argtypes                                             = [pinggy_ref_t]
pinggy_tunnel_is_active.argtypes                                        = [pinggy_ref_t]
pinggy_tunnel_start_web_debugging.argtypes                              = [pinggy_ref_t, pinggy_uint16_t]
pinggy_tunnel_request_primary_forwarding.argtypes                       = [pinggy_ref_t]
pinggy_tunnel_request_additional_forwarding.argtypes                    = [pinggy_ref_t, pinggy_const_char_p_t, pinggy_const_char_p_t]
pinggy_tunnel_start_usage_update.argtypes                               = [pinggy_ref_t]
pinggy_tunnel_stop_usage_update.argtypes                                = [pinggy_ref_t]
pinggy_tunnel_get_current_usages.argtypes                               = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_tunnel_get_greeting_msgs.argtypes                                = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]

#========
#========

pinggy_tunnel_channel_set_data_received_callback.errcheck           = pinggy_error_check
pinggy_tunnel_channel_set_ready_to_send_callback.errcheck           = pinggy_error_check
pinggy_tunnel_channel_set_error_callback.errcheck                   = pinggy_error_check
pinggy_tunnel_channel_set_cleanup_callback.errcheck                 = pinggy_error_check

pinggy_tunnel_channel_set_data_received_callback.restype            = pinggy_bool_t
pinggy_tunnel_channel_set_ready_to_send_callback.restype            = pinggy_bool_t
pinggy_tunnel_channel_set_error_callback.restype                    = pinggy_bool_t
pinggy_tunnel_channel_set_cleanup_callback.restype                  = pinggy_bool_t

pinggy_tunnel_channel_set_data_received_callback.argtypes           = [pinggy_ref_t, pinggy_channel_data_received_cb_t, pinggy_void_p_t]
pinggy_tunnel_channel_set_ready_to_send_callback.argtypes           = [pinggy_ref_t, pinggy_channel_ready_to_send_cb_t, pinggy_void_p_t]
pinggy_tunnel_channel_set_error_callback.argtypes                   = [pinggy_ref_t, pinggy_channel_error_cb_t, pinggy_void_p_t]
pinggy_tunnel_channel_set_cleanup_callback.argtypes                 = [pinggy_ref_t, pinggy_channel_cleanup_cb_t, pinggy_void_p_t]
#========

pinggy_tunnel_channel_accept.errcheck                               = pinggy_error_check
pinggy_tunnel_channel_reject.errcheck                               = pinggy_error_check
pinggy_tunnel_channel_close.errcheck                                = pinggy_error_check
pinggy_tunnel_channel_send.errcheck                                 = pinggy_error_check
pinggy_tunnel_channel_recv.errcheck                                 = pinggy_error_check
pinggy_tunnel_channel_have_data_to_recv.errcheck                    = pinggy_error_check
pinggy_tunnel_channel_have_buffer_to_send.errcheck                  = pinggy_error_check
pinggy_tunnel_channel_is_connected.errcheck                         = pinggy_error_check
pinggy_tunnel_channel_get_type.errcheck                             = pinggy_error_check
pinggy_tunnel_channel_get_dest_port.errcheck                        = pinggy_error_check
pinggy_tunnel_channel_get_dest_host.errcheck                        = pinggy_error_check
pinggy_tunnel_channel_get_dest_host_len.errcheck                    = pinggy_error_check
pinggy_tunnel_channel_get_src_port.errcheck                         = pinggy_error_check
pinggy_tunnel_channel_get_src_host.errcheck                         = pinggy_error_check
pinggy_tunnel_channel_get_src_host_len.errcheck                     = pinggy_error_check
#========

pinggy_tunnel_channel_accept.restype                                = pinggy_bool_t
pinggy_tunnel_channel_reject.restype                                = pinggy_bool_t
pinggy_tunnel_channel_close.restype                                 = pinggy_bool_t
pinggy_tunnel_channel_send.restype                                  = pinggy_raw_len_t
pinggy_tunnel_channel_recv.restype                                  = pinggy_raw_len_t
pinggy_tunnel_channel_have_data_to_recv.restype                     = pinggy_bool_t
pinggy_tunnel_channel_have_buffer_to_send.restype                   = pinggy_uint32_t
pinggy_tunnel_channel_is_connected.restype                          = pinggy_bool_t
pinggy_tunnel_channel_get_type.restype                              = pinggy_uint32_t
pinggy_tunnel_channel_get_dest_port.restype                         = pinggy_uint16_t
pinggy_tunnel_channel_get_dest_host.restype                         = pinggy_const_int_t
pinggy_tunnel_channel_get_dest_host_len.restype                     = pinggy_const_int_t
pinggy_tunnel_channel_get_src_port.restype                          = pinggy_uint16_t
pinggy_tunnel_channel_get_src_host.restype                          = pinggy_const_int_t
pinggy_tunnel_channel_get_src_host_len.restype                      = pinggy_const_int_t

#========

pinggy_tunnel_channel_accept.argtypes                               = [pinggy_ref_t]
pinggy_tunnel_channel_reject.argtypes                               = [pinggy_ref_t, pinggy_char_p_t]
pinggy_tunnel_channel_close.argtypes                                = [pinggy_ref_t]
pinggy_tunnel_channel_send.argtypes                                 = [pinggy_ref_t, pinggy_const_char_p_t, pinggy_raw_len_t]
pinggy_tunnel_channel_recv.argtypes                                 = [pinggy_ref_t, pinggy_char_p_t, pinggy_raw_len_t]
pinggy_tunnel_channel_have_data_to_recv.argtypes                    = [pinggy_ref_t]
pinggy_tunnel_channel_have_buffer_to_send.argtypes                  = [pinggy_ref_t]
pinggy_tunnel_channel_is_connected.argtypes                         = [pinggy_ref_t]
pinggy_tunnel_channel_get_type.argtypes                             = [pinggy_ref_t]
pinggy_tunnel_channel_get_dest_port.argtypes                        = [pinggy_ref_t]
pinggy_tunnel_channel_get_dest_host.argtypes                        = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_tunnel_channel_get_dest_host_len.argtypes                    = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_tunnel_channel_get_src_port.argtypes                         = [pinggy_ref_t]
pinggy_tunnel_channel_get_src_host.argtypes                         = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t]
pinggy_tunnel_channel_get_src_host_len.argtypes                     = [pinggy_ref_t, pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
#========
pinggy_version.errcheck                                             = pinggy_error_check
pinggy_version_len.errcheck                                         = pinggy_error_check
pinggy_git_commit.errcheck                                          = pinggy_error_check
pinggy_git_commit_len.errcheck                                      = pinggy_error_check
pinggy_build_timestamp.errcheck                                     = pinggy_error_check
pinggy_build_timestamp_len.errcheck                                 = pinggy_error_check
pinggy_libc_version.errcheck                                        = pinggy_error_check
pinggy_libc_version_len.errcheck                                    = pinggy_error_check
pinggy_build_os.errcheck                                            = pinggy_error_check
pinggy_build_os_len.errcheck                                        = pinggy_error_check

pinggy_version.restype                                              = pinggy_const_int_t
pinggy_version_len.restype                                          = pinggy_const_int_t
pinggy_git_commit.restype                                           = pinggy_const_int_t
pinggy_git_commit_len.restype                                       = pinggy_const_int_t
pinggy_build_timestamp.restype                                      = pinggy_const_int_t
pinggy_build_timestamp_len.restype                                  = pinggy_const_int_t
pinggy_libc_version.restype                                         = pinggy_const_int_t
pinggy_libc_version_len.restype                                     = pinggy_const_int_t
pinggy_build_os.restype                                             = pinggy_const_int_t
pinggy_build_os_len.restype                                         = pinggy_const_int_t

pinggy_version.argtypes                                             = [pinggy_capa_t, pinggy_char_p_t]
pinggy_version_len.argtypes                                         = [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_git_commit.argtypes                                          = [pinggy_capa_t, pinggy_char_p_t]
pinggy_git_commit_len.argtypes                                      = [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_build_timestamp.argtypes                                     = [pinggy_capa_t, pinggy_char_p_t]
pinggy_build_timestamp_len.argtypes                                 = [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_libc_version.argtypes                                        = [pinggy_capa_t, pinggy_char_p_t]
pinggy_libc_version_len.argtypes                                    = [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
pinggy_build_os.argtypes                                            = [pinggy_capa_t, pinggy_char_p_t]
pinggy_build_os_len.argtypes                                        = [pinggy_capa_t, pinggy_char_p_t, pinggy_capa_p_t]
#========
"""

def pinggy_raise_exception(etype, ewhat):
    global pinggy_thread_local_data
    pinggy_thread_local_data.value = etype.decode('utf-8') + "what: " + ewhat.decode('utf-8')

pinggy_raise_exception = pinggy_on_raise_exception_cb_t(pinggy_raise_exception)

pinggy_set_on_exception_callback(pinggy_raise_exception)


def disable_sdk_log():
    pinggy_set_log_enable(False)
