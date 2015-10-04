import http.server
import socketserver
import os

root = os.getcwd()
print('serving ' + root)

PORT = 8080

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        #print('BEFORE:' + path)
        realpath = path
        if path == '' or path == '/' or path == '/index.html' :
            realpath = '/index.html'
        if realpath.startswith('/'):
            realpath = realpath[1:]
        fullpath = os.path.join(root, realpath)
        #print('AFTER:' + fullpath)
        return fullpath

    def end_headers(self):
        self.send_my_headers()
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def send_my_headers(self):
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

Handler = MyHandler

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
