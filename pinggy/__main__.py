"""
SSH-style command-line entry point for the pinggy SDK.

Usage:
    pinggy [options] [token+type+force@server_address] [tunnel arguments...]

Options:
    -R, --forward-to       TCP/HTTP destination to forward to (default: localhost:80).
                           Accepts formats like [[bindname:]bindport:]localaddress:localport.
    -U, --udp-forward-to   UDP destination to forward to (default: localhost:53).
    -l, --token            User token (overrides any token embedded in server_address).
    -L, --web-debug        Local web debugger port. Format: localport:host:port.

Tunnel arguments (positional, after server_address):
    a:Header:Value         Add a header to the request.
    r:Header               Remove a header from the request.
    u:Header:Value         Update a header in the request.
    b:user:password        Add Basic Auth credentials. May be repeated.
    k:key                  Add a Bearer Auth key. May be repeated.
    w:ip[,ip...]           Allow only these IPs/CIDRs. May be repeated.
    x:https                Redirect HTTP visitors to HTTPS.
    x:xff                  Add X-Forwarded-For header.
    x:fullurl              Add X-Pinggy-Url header with the original URL.
    x:localServerTls[:sni] Treat the local server as TLS (optionally with SNI).
    x:passpreflight        Pass preflight requests through unmodified.
    x:noreverseproxy       Disable reverse proxy mode.
"""

import argparse

from . import BaseTunnelHandler, Tunnel


class _CliHandler(BaseTunnelHandler):
    """Prints public URLs once forwarding succeeds, and reports failures."""

    def tunnel_established(self, urls):
        for url in urls:
            print(url)

    def tunnel_failed(self, msg):
        print(f"Tunnel failed: {msg}")

    def disconnected(self, msg):
        print(f"Tunnel disconnected: {msg}")


def parse_server_address_and_type(server_address):
    """Parse `[token+type+force]@server_address` into its components."""
    force = False
    token = None
    tunnel_type = None
    udp_type = None
    address = None

    parts = server_address.split("@")
    if len(parts) == 2:
        type_and_token, address = parts
        for piece in type_and_token.split("+"):
            orig = piece
            piece = piece.lower()
            if piece == "force":
                force = True
            elif piece == "udp":
                udp_type = piece
            elif piece in ("http", "tcp", "tls", "tlstcp"):
                tunnel_type = piece
            elif piece not in ("qr", "aqr", "auth"):
                if token is None:
                    token = orig
    else:
        address = parts[0]

    return address, tunnel_type, udp_type, token, force


def parse_forward_to(arg_forward_to):
    """Normalise a -R/-U value to `host:port`. Strips bind components if present."""
    if arg_forward_to is None:
        return None
    parts = arg_forward_to.split(":")
    if len(parts) == 1:
        return "localhost:" + parts[0]
    if len(parts) == 2:
        return ":".join(parts)
    return ":".join(parts[-2:])


def parse_local_forward(forward):
    """Pull the local port out of a `localport:host:port` triple (-L value)."""
    if forward is None:
        return 0
    parts = forward.split(":")
    if len(parts) >= 3:
        return int(parts[-3])
    return 0


def main():
    parser = argparse.ArgumentParser(description="Start a Pinggy tunnel.")
    parser.add_argument("-R", "--forward-to", default=None, help="TCP/HTTP address to forward to")
    parser.add_argument("-U", "--udp-forward-to", default=None, help="UDP address to forward to")
    parser.add_argument("-S", "--sni-server-name", default="a.pinggy.io", help=argparse.SUPPRESS)
    parser.add_argument("-l", "--token", default=None, help="Token to use for the tunnel")
    parser.add_argument("-p", "--port", type=int, default=443, help=argparse.SUPPRESS)
    parser.add_argument("-t", "--ignore1", help=argparse.SUPPRESS)
    parser.add_argument("-T", "--ignore2", help=argparse.SUPPRESS)
    parser.add_argument("-n", "--ignore3", help=argparse.SUPPRESS)
    parser.add_argument("-N", "--ignore4", help=argparse.SUPPRESS)
    parser.add_argument("-L", "--web-debug", default=None, help="Web debugger forward (localport:host:port)")
    parser.add_argument(
        "server_info",
        nargs=argparse.REMAINDER,
        help="[token+type+force]@server_address followed by tunnel arguments",
    )

    args = parser.parse_args()

    if not args.server_info:
        parser.error("server_address is required (e.g. token@a.pinggy.io)")

    server_address = args.server_info[0]
    extra_args = args.server_info[1:]

    address, tunnel_type, udp_type, embedded_token, force = parse_server_address_and_type(server_address)

    tcp_forward_to = parse_forward_to(args.forward_to)
    udp_forward_to = parse_forward_to(args.udp_forward_to)
    web_debug_port = parse_local_forward(args.web_debug)

    # Default to HTTP/localhost:80 if no forwarding was specified at all.
    if tunnel_type is None and udp_type is None and tcp_forward_to is None and udp_forward_to is None:
        tunnel_type = "http"
        tcp_forward_to = "localhost:80"
    else:
        if tunnel_type is not None or tcp_forward_to is not None:
            tunnel_type = tunnel_type or "http"
            tcp_forward_to = tcp_forward_to or "localhost:80"
        if udp_type is not None or udp_forward_to is not None:
            udp_type = udp_type or "udp"
            udp_forward_to = udp_forward_to or "localhost:53"

    tun = Tunnel(server_address=address, eventClass=_CliHandler)
    tun.sni_server_name = args.sni_server_name

    if args.token is not None:
        tun.token = args.token
    elif embedded_token is not None:
        tun.token = embedded_token

    if force:
        tun.force = True

    if udp_type is not None:
        tun.add_forwarding(udp_forward_to, type=udp_type)
    if tunnel_type is not None:
        tun.add_forwarding(tcp_forward_to, type=tunnel_type)

    # Aggregate auths / whitelist so that repeated CLI flags accumulate
    # instead of clobbering earlier ones.
    basic_auths = {}
    bearer_auths = []
    ip_whitelist = []

    for arg in extra_args:
        if arg.startswith("a:"):
            header = arg[2:].split(":", 1)
            tun.add_header(header[0], header[1] if len(header) > 1 else "")
        elif arg.startswith("r:"):
            tun.remove_header(arg[2:])
        elif arg.startswith("u:"):
            header = arg[2:].split(":", 1)
            tun.update_header(header[0], header[1] if len(header) > 1 else "")
        elif arg.startswith("b:"):
            creds = arg[2:].split(":", 1)
            if len(creds) > 1:
                basic_auths[creds[0]] = creds[1]
        elif arg.startswith("k:"):
            bearer_auths.append(arg[2:])
        elif arg.startswith("w:"):
            ip_whitelist.extend(arg[2:].split(","))
        elif arg.startswith("x:"):
            option_raw = arg[2:]
            option = option_raw.lower()
            if option == "https":
                tun.httpsonly = True
            elif option == "xff":
                tun.xff = True
            elif option == "fullurl":
                tun.fullrequesturl = True
            elif option.startswith("localservertls"):
                parts = option_raw.split(":", 1)
                tun.localservertls = parts[1] if len(parts) > 1 and parts[1] else "localhost"
            elif option == "passpreflight":
                tun.allowpreflight = True
            elif option == "noreverseproxy":
                tun.reverseproxy = False

    if basic_auths:
        tun.basicauth = basic_auths
    if bearer_auths:
        tun.bearerauth = bearer_auths
    if ip_whitelist:
        tun.ipwhitelist = ip_whitelist

    if web_debug_port:
        tun.webdebugger_port = web_debug_port
        tun.webdebugger = True

    tun.start()


if __name__ == "__main__":
    main()
