import inspect
import unittest
from pinggy.pylib import BaseTunnelHandler, Tunnel, start_tunnel, start_udptunnel
import time

class TestTunnelProperties(unittest.TestCase):
    def setUp(self):
        self.tunnel = Tunnel()

    def test_xff_property(self):
        self.assertTrue(hasattr(self.tunnel, 'xff'))
        self.tunnel.xff = True
        self.assertTrue(self.tunnel.xff)
        self.assertEqual('x:xff', self.tunnel.argument)
        self.tunnel.xff = False
        self.assertFalse(self.tunnel.xff)
        self.assertEqual('', self.tunnel.argument)
        ## set the value using self.tunnel.argument and verify.
        self.tunnel.argument = "x:xff"
        self.assertTrue(self.tunnel.xff)
        self.assertEqual('x:xff', self.tunnel.argument)
        self.tunnel.argument = ""
        self.assertFalse(self.tunnel.xff)
        self.assertEqual('', self.tunnel.argument)

    def test_httpsonly_property(self):
        self.assertTrue(hasattr(self.tunnel, 'httpsonly'))
        self.tunnel.httpsonly = True
        self.assertTrue(self.tunnel.httpsonly)
        self.assertEqual('x:https', self.tunnel.argument)
        self.tunnel.httpsonly = False
        self.assertFalse(self.tunnel.httpsonly)
        self.assertEqual('', self.tunnel.argument)
        ## set the value using self.tunnel.argument and verify.
        self.tunnel.argument = "x:https"
        self.assertTrue(self.tunnel.httpsonly)
        self.assertEqual('x:https', self.tunnel.argument)
        self.tunnel.argument = ""
        self.assertFalse(self.tunnel.httpsonly)
        self.assertEqual('', self.tunnel.argument)

    def test_fullrequesturl_property(self):
        self.assertTrue(hasattr(self.tunnel, 'fullrequesturl'))
        self.tunnel.fullrequesturl = True
        self.assertTrue(self.tunnel.fullrequesturl)
        self.assertEqual('x:fullurl', self.tunnel.argument)
        self.tunnel.fullrequesturl = False
        self.assertFalse(self.tunnel.fullrequesturl)
        self.assertEqual('', self.tunnel.argument)
        ## set the value using self.tunnel.argument and verify.
        self.tunnel.argument = "x:fullurl"
        self.assertTrue(self.tunnel.fullrequesturl)
        self.assertEqual('x:fullurl', self.tunnel.argument)
        self.tunnel.argument = ""
        self.assertFalse(self.tunnel.fullrequesturl)
        self.assertEqual('', self.tunnel.argument)

    def test_allowpreflight_property(self):
        self.assertTrue(hasattr(self.tunnel, 'allowpreflight'))
        self.tunnel.allowpreflight = True
        self.assertTrue(self.tunnel.allowpreflight)
        self.assertEqual('x:passpreflight', self.tunnel.argument)
        self.tunnel.allowpreflight = False
        self.assertFalse(self.tunnel.allowpreflight)
        self.assertEqual('', self.tunnel.argument)
        ## set the value using self.tunnel.argument and verify.
        self.tunnel.argument = "x:passpreflight"
        self.assertTrue(self.tunnel.allowpreflight)
        self.assertEqual('x:passpreflight', self.tunnel.argument)
        self.tunnel.argument = ""
        self.assertFalse(self.tunnel.allowpreflight)
        self.assertEqual('', self.tunnel.argument)

    def test_reverseproxy_property(self):
        self.assertTrue(hasattr(self.tunnel, 'reverseproxy'))
        self.tunnel.reverseproxy = True
        self.assertTrue(self.tunnel.reverseproxy)
        self.assertEqual('', self.tunnel.argument)
        self.tunnel.reverseproxy = False
        self.assertFalse(self.tunnel.reverseproxy)
        self.assertEqual('x:noreverseproxy', self.tunnel.argument)
        ## set the value using self.tunnel.argument and verify.
        self.tunnel.argument = "x:noreverseproxy"
        self.assertFalse(self.tunnel.reverseproxy)
        self.assertEqual('x:noreverseproxy', self.tunnel.argument)
        self.tunnel.argument = ""
        self.assertTrue(self.tunnel.reverseproxy)
        self.assertEqual('', self.tunnel.argument)

    def test_ipwhitelist_property(self):
        self.assertTrue(hasattr(self.tunnel, 'ipwhitelist'))
        self.tunnel.ipwhitelist = ['1.2.3.4/32', '5.6.7.8/24']
        self.assertEqual(self.tunnel.ipwhitelist, ['1.2.3.4/32', '5.6.7.8/24'])
        self.assertEqual('w:1.2.3.4/32,5.6.7.8/24', self.tunnel.argument)
        self.tunnel.ipwhitelist = '9.9.9.9/32'
        self.assertEqual(self.tunnel.ipwhitelist, ['9.9.9.9/32'])
        self.assertEqual('w:9.9.9.9/32', self.tunnel.argument)
        self.tunnel.ipwhitelist = []
        self.assertEqual(self.tunnel.ipwhitelist, [])
        self.assertEqual('', self.tunnel.argument)
        # Test with IPs without slash and with IPv6
        self.tunnel.ipwhitelist = ['8.8.8.8', '2001:db8::1/64']
        self.assertEqual(self.tunnel.ipwhitelist, ['8.8.8.8', '2001:db8::1/64'])
        self.assertEqual('w:8.8.8.8,2001:db8::1/64', self.tunnel.argument)
        self.tunnel.ipwhitelist = '123.123.123.123'
        self.assertEqual(self.tunnel.ipwhitelist, ['123.123.123.123'])
        self.assertEqual('w:123.123.123.123', self.tunnel.argument)

    def test_headermodification_property(self):
        self.assertTrue(hasattr(self.tunnel, 'headermodification'))
        # Set header modifications directly
        self.tunnel.headermodification = [
            {
                "type": "remove",
                "key": "Accept"
            },
            {
                "type": "add",
                "key": "User-Agent",
                "value": ["TestAgent"]
            }
        ]
        self.assertEqual('r:Accept a:User-Agent:TestAgent', self.tunnel.argument)
        # Add a header using addHeader
        self.tunnel.headermodification = None
        self.assertEqual('', self.tunnel.argument)
        self.tunnel.add_header('X-Test', 'Value one')
        self.assertEqual('"a:X-Test:Value one"', self.tunnel.argument)
        # Remove a header using removeHeader
        self.tunnel.headermodification = None
        self.tunnel.remove_header('X-Remove')
        self.assertEqual('r:X-Remove', self.tunnel.argument)
        # Update a header using updateHeader
        self.tunnel.headermodification = None
        self.tunnel.update_header('X-Update', 'NewValue')
        # self.assertIn('a:X-Update:NewValue', self.tunnel.headermodification)
        self.assertEqual('u:X-Update:NewValue', self.tunnel.argument)

    def test_basicauth_property(self):
        self.assertTrue(hasattr(self.tunnel, 'basicauth'))
        # Set basic auth with a dictionary
        self.tunnel.basicauth = {'user1': 'pass1', 'user2': 'pass two'}
        self.assertEqual(self.tunnel.basicauth, [{"username":'user1', "password": 'pass1'}, {"username":'user2', "password": 'pass two'}])
        self.assertEqual("b:user1:pass1 \"b:user2:pass two\"", self.tunnel.argument)
        # Set basic auth with a single user
        self.tunnel.basicauth = {'admin': 'secret'}
        self.assertEqual(self.tunnel.basicauth, [{'username': 'admin', 'password': 'secret'}])
        self.assertEqual('b:admin:secret', self.tunnel.argument)
        # Remove basic auth
        self.tunnel.basicauth = []
        self.assertEqual([], self.tunnel.basicauth)
        self.assertEqual('', self.tunnel.argument)
        ## set the value using self.tunnel.argument and verify.
        self.tunnel.argument = "b:user:pass"
        self.assertEqual(self.tunnel.basicauth, [{'username': 'user', 'password': 'pass'}])
        self.assertEqual('b:user:pass', self.tunnel.argument)
        self.tunnel.argument = ""
        self.assertEqual([], self.tunnel.basicauth)
        self.assertEqual('', self.tunnel.argument)
        with self.assertRaises(Exception):
            self.tunnel.basicauth = "b:a:b"

        # self.assertEqual("b:a:b", self.tunnel.basicauth)
        # self.assertEqual('', self.tunnel.argument)

    def test_bearerauth_property(self):
        self.assertTrue(hasattr(self.tunnel, 'bearerauth'))
        # Set bearer auth with a list
        self.tunnel.bearerauth = ['key1', 'key2']
        self.assertEqual(self.tunnel.bearerauth, ['key1', 'key2'])
        self.assertEqual('k:key1 k:key2', self.tunnel.argument)
        # Set bearer auth with a single string
        self.tunnel.bearerauth = 'singlekey'
        self.assertEqual(self.tunnel.bearerauth, ['singlekey'])
        self.assertEqual('k:singlekey', self.tunnel.argument)
        # Remove bearer auth
        self.tunnel.bearerauth = None
        self.assertEqual([], self.tunnel.bearerauth)
        self.assertEqual('', self.tunnel.argument)
        ## set the value using self.tunnel.argument and verify.
        self.tunnel.argument = "k:testkey"
        self.assertEqual(self.tunnel.bearerauth, ['testkey'])
        self.assertEqual('k:testkey', self.tunnel.argument)
        self.tunnel.argument = ""
        self.assertEqual([], self.tunnel.bearerauth)
        self.assertEqual('', self.tunnel.argument)

    def test_localservertls_property(self):
        self.assertTrue(hasattr(self.tunnel, 'localservertls'))
        # Default should be empty
        self.assertEqual("", self.tunnel.localservertls)
        # Set localservertls
        self.tunnel.localservertls = "localhost"
        self.assertEqual("localhost", self.tunnel.localservertls )
        self.assertEqual('x:localServerTls:localhost', self.tunnel.argument)
        # Set localservertls
        self.tunnel.localservertls = "test.local"
        self.assertEqual(self.tunnel.localservertls, "test.local")
        self.assertEqual('x:localServerTls:test.local', self.tunnel.argument)
        # Reset localservertls
        self.tunnel.localservertls = None
        self.assertEqual("", self.tunnel.localservertls)
        # Set localservertls
        self.tunnel.localservertls = "SomeValue"
        self.assertEqual(self.tunnel.localservertls, "SomeValue")
        self.assertEqual('x:localServerTls:SomeValue', self.tunnel.argument)
        # Reset localservertls
        self.tunnel.localservertls = ""
        self.assertEqual("", self.tunnel.localservertls)
        ## set the value using self.tunnel.argument and verify.
        self.tunnel.argument = "x:localServerTls:argumentValue"
        self.assertEqual(self.tunnel.localservertls, "argumentValue")
        self.assertEqual('x:localServerTls:argumentValue', self.tunnel.argument)
        self.tunnel.argument = ""
        self.assertEqual("", self.tunnel.localservertls)
        self.assertEqual('', self.tunnel.argument)

class TestAfterTunnelStarted(unittest.TestCase):
    def test_testIpWhiteList(self):
        tunnel = start_tunnel(ipwhitelist="10.0.0.0/10", webdebuggerport=4300)
        time.sleep(3)
        tunnel.stop()


class TestLegacyCompat(unittest.TestCase):
    """
    Legacy API kept for backwards compatibility. New libpinggy fused several
    flow steps and dropped several callbacks; these tests pin down that legacy
    user code keeps running (no crashes, no AttributeError) even though the
    legacy surface is no longer documented.
    """

    def test_legacy_methods_do_not_crash(self):
        tunnel = Tunnel()
        # connect() and request_primary_forwarding() are no-ops in the new
        # flow but must keep their old return contract.
        self.assertTrue(tunnel.connect())
        self.assertTrue(tunnel.request_primary_forwarding())

    def test_legacy_callback_stubs_present(self):
        # Legacy subclasses call super().<callback>() — those stubs must exist
        # on BaseTunnelHandler even though the lib no longer fires them.
        handler = BaseTunnelHandler(tunnel=None)
        self.assertIsNone(handler.authenticated())
        self.assertIsNone(handler.authentication_failed(["err"]))
        self.assertIsNone(handler.primary_forwarding_succeeded())
        self.assertIsNone(handler.primary_forwarding_failed("msg"))

    def test_legacy_tcp_forward_to_engages_legacy_mode(self):
        tunnel = Tunnel()
        tunnel.tcp_forward_to = "localhost:8080"
        self.assertEqual(tunnel.tcp_forward_to, "localhost:8080")
        # Once a legacy property is set, mixing with the new API must error.
        with self.assertRaises(Exception):
            tunnel.add_forwarding("localhost:9090")
        with self.assertRaises(Exception):
            tunnel.forwardings = "localhost:9090"

    def test_legacy_udp_forward_to_engages_legacy_mode(self):
        tunnel = Tunnel()
        tunnel.udp_type = "udp"
        tunnel.udp_forward_to = 53
        self.assertEqual(tunnel.udp_forward_to, "localhost:53")
        with self.assertRaises(Exception):
            tunnel.add_forwarding(80, type="http")

    def test_new_forwardings_blocks_legacy(self):
        tunnel = Tunnel()
        tunnel.forwardings = "localhost:80"
        with self.assertRaises(Exception):
            tunnel.tcp_forward_to = "localhost:9090"
        with self.assertRaises(Exception):
            tunnel.type = "tcp"

    def test_new_add_forwarding_blocks_legacy(self):
        tunnel = Tunnel()
        tunnel.add_forwarding("localhost:80")
        with self.assertRaises(Exception):
            tunnel.tcp_forward_to = "localhost:9090"

    def test_start_tunnel_signature_is_backward_compatible(self):
        # The old published `start_tunnel` had this positional order:
        #   forwardto, type, token, force, ipwhitelist, basicauth,
        #   bearerauth, headermodification, webdebuggerport, xff,
        #   httpsonly, fullrequesturl, allowpreflight, reverseproxy,
        #   serveraddress
        # Any new params must be appended after that block.
        params = list(inspect.signature(start_tunnel).parameters)
        legacy_prefix = [
            "forwardto", "type", "token", "force", "ipwhitelist",
            "basicauth", "bearerauth", "headermodification",
            "webdebuggerport", "xff", "httpsonly", "fullrequesturl",
            "allowpreflight", "reverseproxy", "serveraddress",
        ]
        self.assertEqual(params[: len(legacy_prefix)], legacy_prefix)
        # New params live at the tail.
        for new_param in ("udpforwardto", "localservertls", "autoreconnect", "eventclass"):
            self.assertIn(new_param, params)

    def test_start_udptunnel_signature_is_backward_compatible(self):
        params = list(inspect.signature(start_udptunnel).parameters)
        legacy_prefix = ["forwardto", "token", "force", "ipwhitelist", "webdebuggerport", "serveraddress"]
        self.assertEqual(params[: len(legacy_prefix)], legacy_prefix)


class TestAddCallback(unittest.TestCase):
    """
    `Tunnel.add_callback` lets you wire a function for a tunnel event without
    subclassing `BaseTunnelHandler`. It must also win over a method defined on
    a custom handler class.
    """

    def test_add_callback_fires_when_event_dispatches(self):
        tunnel = Tunnel()
        captured = []
        tunnel.add_callback("tunnel_failed", lambda msg: captured.append(msg))
        # Drive the C-callback dispatcher directly with a fake msg.
        tunnel._Tunnel__func_tunnel_failed(None, 0, b"oops")
        self.assertEqual(captured, ["oops"])

    def test_add_callback_overrides_eventclass_method(self):
        class HandlerThatLogs(BaseTunnelHandler):
            def __init__(self, tunnel):
                super().__init__(tunnel)
                self.calls = []

            def disconnected(self, msg):
                self.calls.append(("class", msg))

        tunnel = Tunnel(eventClass=HandlerThatLogs)
        captured = []
        tunnel.add_callback("disconnected", lambda msg: captured.append(("cb", msg)))
        tunnel._Tunnel__func_disconnected(None, 0, b"bye", 0, None)
        # Only the callback should fire, not the class method.
        self.assertEqual(captured, [("cb", "bye")])
        self.assertEqual(tunnel._Tunnel__eventHandler.calls, [])

    def test_add_callback_supports_multiple_events(self):
        tunnel = Tunnel()
        events = []
        tunnel.add_callback("tunnel_failed", lambda msg: events.append(("failed", msg)))
        tunnel.add_callback("disconnected", lambda msg: events.append(("disc", msg)))
        tunnel._Tunnel__func_tunnel_failed(None, 0, b"a")
        tunnel._Tunnel__func_disconnected(None, 0, b"b", 0, None)
        self.assertEqual(events, [("failed", "a"), ("disc", "b")])

    def test_on_event_attribute_assignment_routes_to_handler(self):
        tunnel = Tunnel()
        captured = []
        tunnel.on_tunnel_failed = lambda msg: captured.append(msg)
        tunnel._Tunnel__func_tunnel_failed(None, 0, b"oops")
        self.assertEqual(captured, ["oops"])

    def test_on_event_attribute_get_returns_installed_callback(self):
        tunnel = Tunnel()
        fn = lambda msg: None
        tunnel.on_disconnected = fn
        self.assertIs(tunnel.on_disconnected, fn)

    def test_on_event_attribute_overrides_eventclass_method(self):
        class HandlerThatLogs(BaseTunnelHandler):
            def __init__(self, tunnel):
                super().__init__(tunnel)
                self.calls = []

            def disconnected(self, msg):
                self.calls.append(("class", msg))

        tunnel = Tunnel(eventClass=HandlerThatLogs)
        captured = []
        tunnel.on_disconnected = lambda msg: captured.append(msg)
        tunnel._Tunnel__func_disconnected(None, 0, b"bye", 0, None)
        self.assertEqual(captured, ["bye"])
        self.assertEqual(tunnel._Tunnel__eventHandler.calls, [])

    def test_setting_non_on_attribute_still_works(self):
        # Sanity: the __setattr__ shim must not break regular attribute use.
        tunnel = Tunnel()
        tunnel.token = "hello"
        self.assertEqual(tunnel.token, "hello")
        tunnel.scratch = 123  # arbitrary user attribute
        self.assertEqual(tunnel.scratch, 123)


if __name__ == '__main__':
    unittest.main()
