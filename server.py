
"""Serve the DDSS static client from the public directory."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
PUBLIC_DIRECTORY = Path(__file__).parent / "public"


def create_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    """Create an HTTP server configured to serve files from ``public``."""
    handler = partial(SimpleHTTPRequestHandler, directory=str(PUBLIC_DIRECTORY))
    return ThreadingHTTPServer((host, port), handler)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the DDSS static client.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Interface to bind to.")
    parser.add_argument(
        "--port",
        default=DEFAULT_PORT,
        type=int,
        help="TCP port to listen on.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with create_server(args.host, args.port) as server:
        address = server.server_address
        print(f"Serving {PUBLIC_DIRECTORY} at http://{address[0]}:{address[1]}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")


if __name__ == "__main__":
    main()
