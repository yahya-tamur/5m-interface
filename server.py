from http.server import HTTPServer, BaseHTTPRequestHandler
from env import server_address, server_port
from collections import defaultdict
from pathlib import Path
import os

from tcp_interface import commands, send_to_printer

server_path = "./website"

files = [
    "index.html",
    "roboto.css",
    "roboto.woff2",
    "theme.css",
    "update.js",
    "bundle.js",
]

file_paths = {file: f"{server_path}/{file}" for file in files}
file_paths[""] = f"{server_path}/index.html"


class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        if (w := self.path.find("?")) != -1:
            path = self.path[1:w]
            params = self.path[w + 1 :]
        else:
            path = self.path[1:]
            params = ""

        param_dict = defaultdict(str)
        for lr in params.split("&"):
            if (w := lr.find("=")) != -1:
                param_dict[lr[:w]] = lr[w + 1 :]

        if (file := file_paths.get(path)) is not None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(Path(file).read_bytes())

        elif path in commands:
            code, resp = send_to_printer(path, param_dict["printer-ip"])
            if code == 200:

                resp = resp.decode("ascii")
                print(resp)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(resp.encode("ascii"))
            else:
                self.send_response(code)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()


httpd = HTTPServer((server_address, server_port), Serv)

print(
    f"Hosting on http://{server_address}:{server_port}?printer-ip=<your printer's ip address>"
)

httpd.serve_forever()
