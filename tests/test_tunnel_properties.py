import unittest
from pinggy.pylib import Tunnel, start_tunnel

class TestTunnelProperties(unittest.TestCase):
    def setUp(self):
        self.tunnel = Tunnel()

    def test_xff_property(self):
        self.assertTrue(hasattr(self.tunnel, 'xff'))
        self.tunnel.xff = True
        self.assertTrue(self.tunnel.xff)
        self.assertEqual(b'x:xff', self.tunnel.getProcessedArguments())
        self.tunnel.xff = False
        self.assertFalse(self.tunnel.xff)
        self.assertEqual(b'', self.tunnel.getProcessedArguments())

    def test_httpsonly_property(self):
        self.assertTrue(hasattr(self.tunnel, 'httpsonly'))
        self.tunnel.httpsonly = True
        self.assertTrue(self.tunnel.httpsonly)
        self.assertEqual(b'x:https', self.tunnel.getProcessedArguments())
        self.tunnel.httpsonly = False
        self.assertFalse(self.tunnel.httpsonly)
        self.assertEqual(b'', self.tunnel.getProcessedArguments())

    def test_fullrequesturl_property(self):
        self.assertTrue(hasattr(self.tunnel, 'fullrequesturl'))
        self.tunnel.fullrequesturl = True
        self.assertTrue(self.tunnel.fullrequesturl)
        self.assertEqual(b'x:fullurl', self.tunnel.getProcessedArguments())
        self.tunnel.fullrequesturl = False
        self.assertFalse(self.tunnel.fullrequesturl)
        self.assertEqual(b'', self.tunnel.getProcessedArguments())

    def test_allowpreflight_property(self):
        self.assertTrue(hasattr(self.tunnel, 'allowpreflight'))
        self.tunnel.allowpreflight = True
        self.assertTrue(self.tunnel.allowpreflight)
        self.assertEqual(b'x:passpreflight', self.tunnel.getProcessedArguments())
        self.tunnel.allowpreflight = False
        self.assertFalse(self.tunnel.allowpreflight)
        self.assertEqual(b'', self.tunnel.getProcessedArguments())

    def test_reverseproxy_property(self):
        self.assertTrue(hasattr(self.tunnel, 'reverseproxy'))
        self.tunnel.reverseproxy = True
        self.assertTrue(self.tunnel.reverseproxy)
        self.assertEqual(b'', self.tunnel.getProcessedArguments())
        self.tunnel.reverseproxy = False
        self.assertFalse(self.tunnel.reverseproxy)
        self.assertEqual(b'x:noreverseproxy', self.tunnel.getProcessedArguments())

    def test_ipwhitelist_property(self):
        self.assertTrue(hasattr(self.tunnel, 'ipwhitelist'))
        self.tunnel.ipwhitelist = ['1.2.3.4/32', '5.6.7.8/24']
        self.assertEqual(self.tunnel.ipwhitelist, ['1.2.3.4/32', '5.6.7.8/24'])
        self.assertEqual(b'w:1.2.3.4/32,5.6.7.8/24', self.tunnel.getProcessedArguments())
        self.tunnel.ipwhitelist = '9.9.9.9/32'
        self.assertEqual(self.tunnel.ipwhitelist, ['9.9.9.9/32'])
        self.assertEqual(b'w:9.9.9.9/32', self.tunnel.getProcessedArguments())
        self.tunnel.ipwhitelist = []
        self.assertEqual(self.tunnel.ipwhitelist, [])
        self.assertEqual(b'', self.tunnel.getProcessedArguments())
        # Test with IPs without slash and with IPv6
        self.tunnel.ipwhitelist = ['8.8.8.8', '2001:db8::1/64']
        self.assertEqual(self.tunnel.ipwhitelist, ['8.8.8.8', '2001:db8::1/64'])
        self.assertEqual(b'w:8.8.8.8,2001:db8::1/64', self.tunnel.getProcessedArguments())
        self.tunnel.ipwhitelist = '123.123.123.123'
        self.assertEqual(self.tunnel.ipwhitelist, ['123.123.123.123'])
        self.assertEqual(b'w:123.123.123.123', self.tunnel.getProcessedArguments())

    def test_headermodification_property(self):
        self.assertTrue(hasattr(self.tunnel, 'headermodification'))
        # Set header modifications directly
        self.tunnel.headermodification = ['r:Accept', 'a:User-Agent:TestAgent']
        self.assertEqual(self.tunnel.headermodification, ['r:Accept', 'a:User-Agent:TestAgent'])
        self.assertEqual(b'r:Accept a:User-Agent:TestAgent', self.tunnel.getProcessedArguments())
        # Add a header using addHeader
        self.tunnel.headermodification = None
        self.tunnel.addHeader('X-Test', 'Value one')
        self.assertIn("a:X-Test:Value one", self.tunnel.headermodification)
        self.assertEqual(b"'a:X-Test:Value one'", self.tunnel.getProcessedArguments())
        # Remove a header using removeHeader
        self.tunnel.headermodification = None
        self.tunnel.removeHeader('X-Remove')
        self.assertIn('r:X-Remove', self.tunnel.headermodification)
        self.assertEqual(b'r:X-Remove', self.tunnel.getProcessedArguments())
        # Update a header using updateHeader
        self.tunnel.headermodification = None
        self.tunnel.updateHeader('X-Update', 'NewValue')
        self.assertIn('a:X-Update:NewValue', self.tunnel.headermodification)
        self.assertEqual(b'a:X-Update:NewValue', self.tunnel.getProcessedArguments())

    def test_basicauth_property(self):
        self.assertTrue(hasattr(self.tunnel, 'basicauth'))
        # Set basic auth with a dictionary
        self.tunnel.basicauth = {'user1': 'pass1', 'user2': 'pass two'}
        self.assertEqual(self.tunnel.basicauth, {'user1': 'pass1', 'user2': 'pass two'})
        self.assertEqual(b"b:user1:pass1 'b:user2:pass two'", self.tunnel.getProcessedArguments())
        # Set basic auth with a single user
        self.tunnel.basicauth = {'admin': 'secret'}
        self.assertEqual(self.tunnel.basicauth, {'admin': 'secret'})
        self.assertEqual(b'b:admin:secret', self.tunnel.getProcessedArguments())
        # Remove basic auth
        self.tunnel.basicauth = None
        self.assertIsNone(self.tunnel.basicauth)
        self.assertEqual(b'', self.tunnel.getProcessedArguments())

    def test_bearerauth_property(self):
        self.assertTrue(hasattr(self.tunnel, 'bearerauth'))
        # Set bearer auth with a list
        self.tunnel.bearerauth = ['key1', 'key2']
        self.assertEqual(self.tunnel.bearerauth, ['key1', 'key2'])
        self.assertEqual(b'k:key1 k:key2', self.tunnel.getProcessedArguments())
        # Set bearer auth with a single string
        self.tunnel.bearerauth = 'singlekey'
        self.assertEqual(self.tunnel.bearerauth, ['singlekey'])
        self.assertEqual(b'k:singlekey', self.tunnel.getProcessedArguments())
        # Remove bearer auth
        self.tunnel.bearerauth = None
        self.assertIsNone(self.tunnel.bearerauth)
        self.assertEqual(b'', self.tunnel.getProcessedArguments())

class TestAfterTunnelStarted(unittest.TestCase):
    def test_testIpWhiteList(self):
        tunnel = start_tunnel(ipwhitelist="10.0.0.0/10", webdebuggerport=4300)



if __name__ == '__main__':
    unittest.main()
