import threading
import time
import pinggy

# pinggy.disableLog()

class TunnelHandler(pinggy.BaseTunnelHandler):
    def primary_forwarding_succeeded(self):
        tunnel:pinggy.Tunnel = self.get_tunnel()
        print(tunnel.urls)
        # tunnel.request_additional_forwarding("y.example.com:0", "l:3000")


tunnel = pinggy.Tunnel("t.pinggy.io:443", TunnelHandler)
tunnel.server_address = "t.pinggy.io:443"
tunnel.sni_server_name = "t.pinggy.io"
# tunnel.server_address = "localhost:7878"
# tunnel.sni_server_name = "example.com"
# tunnel.insecure = True
tunnel.advanced_parsing = True
tunnel.tcp_forward_to = "localhost:4000"


print("server_address       :", tunnel.server_address)
print("token                :", tunnel.token)
print("type                 :", tunnel.type)
print("udp_type             :", tunnel.udp_type)
print("tcp_forward_to       :", tunnel.tcp_forward_to)
print("udp_forward_to       :", tunnel.udp_forward_to)
# print("enable_web_debugger  :", tunnel.enable_web_debugger)
# print("web_debugger_port    :", tunnel.web_debugger_port)
# print("print_continue_usage :", tunnel.print_continue_usage)
print("force                :", tunnel.force)
print("argument             :", tunnel.argument)
print("advanced_parsing     :", tunnel.advanced_parsing)
print("ssl                  :", tunnel.ssl)
print("sni_server_name      :", tunnel.sni_server_name)
print("insecure             :", tunnel.insecure)

# tunnel.start()

def starttune(tunnel: pinggy.Tunnel):
    tunnel.connect()
    tunnel.request_primary_forwarding()
    tunnel.serve_tunnel()
    # tunnel.start_with_c()

# tunnel.start_with_c()

# tunnel2 = pinggy.Tunnel()
# tunnel2.server_address = "t.pinggy.io:443"
# tunnel2.sni_server_name = "t.pinggy.io"
# tunnel2.tcp_forward_to = "l:4000"


t = threading.Thread(target=starttune, args=(tunnel,))
# t2 = threading.Thread(target=starttune, args=(tunnel2,))
t.start()
# t2.start()

print("going to sleep")

time.sleep(150)

print("stoping tunnel")

tunnel.stop()

t.join()
