from .pylib import *
import argparse
from pinggy import Tunnel


# main function that can read command line arguments and use the same to call start_tunnel followed by printing the URLs
# The options are:
# The command format is:
# pinggy [options] [token+][type+][force+]@server_address [arguments]
# -s, --server-address: The server address to connect to (default: "a.pinggy.io")
# -R, --tcp-forward-to: The TCP address to forward to (default: "localhost:80"). It supports formats like [[[bindname:]bindport:]]localaddress:]localport
# -U, --udp-forward-to: The UDP address to forward to (default: "localhost:53"). It supports formats like [[[bindname:]bindport:]]localaddress:]localport
# -S, --sni-server-name: The SNI server name to use (default: "a.pinggy.io")
# -l, --token: The token to use (default: None)
# -p, --port: The port to connect to (default: 443)
# Arguments are:
# a:HeaderName:HeaderValue  Add a header to the request
# r:HeaderName Remove a header from the request
# u:HeaderName:HeaderValue Update a header in the request. It is equivalent to r:HeaderName followed by a:HeaderName:HeaderValue
# b:username:password Set the basic authentication credentials
# k:key Set the key for bearer key authentication
# w:[IP1[,IP2[,IP3..]]] Set the allowed IPs for the tunnel
# x:https Force the tunnel to use HTTPS
# x:xff Force pinggy to use add X-Forwarded-For header
# x:fullurl Pinggy will put the full URL in the  X-Pinggy-Url header
# x:localServerTls[:serverName] Assume the local server is using TLS, and optionally set the server name for SNI
# x:passpreflight Allow preflight requests to pass through without any auhentication
# x:noreverseproxy Do not use reverse proxy for the tunnel

def parse_server_address_and_type(server_address):
    force = False
    token = None
    tunnel_type = None
    udp_type = None
    address = None

    parts = server_address.lower().split("@")
    if len(parts) == 2:
        type_and_token, address = parts
        type_and_token_parts = type_and_token.split("+")
        for p in type_and_token_parts:
            if p == "force":
                force = True
            elif p == "udp":
                udp_type = p
            elif p == "http" or p == "tcp" or p == "tls" or p == "tlstcp":
                tunnel_type = p
            elif p != "qr" and p != "aqr" and p != "auth":
                if token is None:
                    token = p

    else:
        address = parts[0]

    if tunnel_type is None and udp_type is None:
        tunnel_type = "http"

    return address, tunnel_type, udp_type, token, force

def main():

    parser = argparse.ArgumentParser(description="Start a Pinggy tunnel with specified options.")
    parser.add_argument("-s", "--server-address", default="a.pinggy.io", help="Server address to connect to")
    parser.add_argument("-R", "--forward-to", default="localhost:80", help="TCP address to forward to")
    # parser.add_argument("-U", "--udp-forward-to", default=None, help="UDP address to forward to")
    parser.add_argument("-S", "--sni-server-name", default="a.pinggy.io", help="SNI server name to use")
    parser.add_argument("-l", "--token", default=None, help="Token to use for the tunnel")
    parser.add_argument("-p", "--port", type=int, default=443, help="Port to connect to")

    args, unknown = parser.parse_known_args()

    tun = Tunnel(server_address=args.server_address)
    # tun.tcp_forward_to = args.tcp_forward_to
    # tun.udp_forward_to = args.udp_forward_to
    tun.sni_server_name = args.sni_server_name
    # tun.token = args.token
    arg_forward_to = args.forward_to
    if arg_forward_to is not None:
        parts = arg_forward_to.split(":")
        if len(parts) == 1:
            arg_forward_to = "localhost:" + parts[0]
        elif len(parts) == 2:
            arg_forward_to = ":".join(parts)
        elif len(parts) > 2:
            arg_forward_to = ":".join(parts[-2:])

    address, tunnel_type, udp_type, token, force = parse_server_address_and_type(args.server_address)
    if address is not None:
        tun.server_address = address

    if tunnel_type is not None:
        tun.type = tunnel_type
        tun.tcp_forward_to = arg_forward_to

    if udp_type is not None:
        tun.udp_forward_to = arg_forward_to

    if token is not None:
        tun.token = token
    if args.token is not None:
        tun.token = args.token

    if force:
        tun.force = True

    # Process additional arguments
    for arg in unknown:
        if arg.startswith("a:"):
            header = arg[2:].split(":")
            tun.add_header(header[0], header[1] if len(header) > 1 else "")
        elif arg.startswith("r:"):
            tun.remove_header(arg[2:])
        elif arg.startswith("u:"):
            header = arg[2:].split(":")
            tun.update_header(header[0], header[1] if len(header) > 1 else "")
        elif arg.startswith("b:"):
            credentials = arg[2:].split(":")
            tun.set_basic_auth(credentials[0], credentials[1] if len(credentials) > 1 else "")
        elif arg.startswith("k:"):
            tun.set_bearer_key(arg[2:])
        elif arg.startswith("w:"):
            ips = arg[2:].split(",")
            tun.set_allowed_ips(ips)
        elif arg.startswith("x:"):
            option = arg[2:]
            if option == "https":
                tun.ssl = True
            elif option == "xff":
                tun.use_xff_header = True
            elif option == "fullurl":
                tun.full_url_in_header = True
            elif option.startswith("localServerTls"):
                parts = option.split(":")
                tun.local_server_tls = True
                if len(parts) > 1:
                    tun.sni_server_name = parts[1]
            elif option == "passpreflight":
                tun.pass_preflight = True
            elif option == "noreverseproxy":
                tun.use_reverse_proxy = False

    if not tun.connect():
        print("Failed to connect to the server.")
        return
    if not tun.request_primary_forwarding():
        print("Failed to request primary forwarding.")
        return
    print("Tunnel URLs:", tun.urls)
    tun.start()

if __name__ == "__main__":
    main()