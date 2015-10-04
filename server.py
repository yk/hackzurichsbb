import http.server
import socketserver
import os
import webapi
import json
import urllib

root = os.getcwd()
print('serving ' + root)

PORT = 8888


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path is not None and self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.handle_api()
            return
        return super().do_GET()

    def end_headers(self):
        self.send_my_headers()
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.do_GET()

    def send_my_headers(self):
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

    def handle_api(self):
        path = self.path[5:].split('/')
        if path[0].startswith('search'):
            qs = path[0].split('?')[1]
            params = urllib.parse.parse_qs(qs)
            reslist = webapi.search_name(params['query'])
            self.wfile.write(json.dumps(reslist).encode())
            return
        elif path[0].startswith('route'):
            qs = path[0].split('?')[1]
            params = urllib.parse.parse_qs(qs)
            reslist = webapi.get_route(params)
            self.wfile.write(json.dumps({'connections': reslist}).encode())
            return


Handler = MyHandler

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
