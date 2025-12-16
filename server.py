from http.server import HTTPServer, BaseHTTPRequestHandler
from env import server_address, server_port
from collections import defaultdict
from pathlib import Path
import os

from tcp_interface import commands, send_to_printer

server_path = './m-ui/test/'


file_paths ={file: file for file in os.listdir(server_path)}
file_paths[""] = 'index.html'
#file_paths = {'': 'm-ui/test/index.html', \
        #'bundle.js': 'm
        #'schema': 'schema.html', \
        #'index': 'index.html', \
        #'index.css': 'index.css', \
        #'jquery.js': 'jquery-3.7.1.min.js' \
        #}

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        if (w := self.path.find('?')) != -1:
            path = self.path[1:w]
            params = self.path[w+1:]
        else:
            path = self.path[1:]
            params = ''

        param_dict = defaultdict(str)
        for lr in params.split('&'):
            if (w := lr.find('=')) != -1:
                param_dict[lr[:w]] = lr[w+1:]

        if (file := file_paths.get(path)) is not None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(Path(f"{server_path}{file}").read_bytes())

        elif path in commands:
            code, resp = send_to_printer(path, param_dict['printer-ip'])
            if code == 200:

                resp = resp.decode('ascii')
                print(resp)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(resp.encode('ascii'))
            else:
                self.send_response(code)
                self.end_headers()


        else:
            self.send_response(404)
            self.end_headers()

httpd = HTTPServer((server_address, server_port),Serv)

print(f"Hosting on http://{server_address}:{server_port}?printer-ip=<your printer's ip address>")

httpd.serve_forever()

