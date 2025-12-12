from http.server import HTTPServer, BaseHTTPRequestHandler

from tcp_interface import commands, send_to_printer

from env import printer_ip, server_address, server_port

file_paths = {'': 'index.html', \
        'schema': 'schema.html', \
        'index': 'index.html', \
        'index.css': 'index.css', \
        'jquery.js': 'jquery-3.7.1.min.js' \
        }

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        path = self.path[1:]

        if (file := file_paths.get(path)) is not None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(open(file).read(), 'utf-8'))

        elif path in commands:
            _code, resp = send_to_printer(path, printer_ip)
            resp = resp.decode('ascii')
            print(resp)
            # do nicer printing later?
            resp = resp[resp.find('\r\n')+2:]
            print(resp)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(resp.encode('ascii'))

        else:
            self.send_response(404)
            self.end_headers()

httpd = HTTPServer((server_address, server_port),Serv)

print(f"Hosting on http://{server_address}:{server_port}")

httpd.serve_forever()

