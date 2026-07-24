# server.py
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 80

server = HTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
print(f"Serving http://0.0.0.0:{PORT}")
server.serve_forever()