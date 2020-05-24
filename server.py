import http.server
import socketserver
import threading
from functools import partial
from urllib.parse import urlparse
from urllib.parse import parse_qs

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, database, *args, **kwargs):
        self.database = database
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()
        __length = self.headers['Content-Length']
        self.data_string = ""
        if __length:
            self.data_string = self.rfile.read(int(__length))

        # Extract query param
        print(f"Request type: GET")
        print(f"Received path: {self.path}")
        print(f"Received query: {urlparse(self.path).query}")
        print(f"Received body: {self.data_string}")

        self.database.push(dict(method = "get",
                                path = self.path,
                                query = urlparse(self.path).query,
                                body = self.data_string))

        # Some custom HTML code, possibly generated by another function
        html = ""

        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(html, "utf8"))

        return

    def do_POST(self):
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        __length = self.headers['Content-Length']
        self.data_string = ""
        if __length:
            self.data_string = self.rfile.read(int(__length))

        # Extract query param
        print(f"Request type: POST")
        print(f"Received path: {self.path}")
        print(f"Received query: {urlparse(self.path).query}")
        print(f"Received body: {self.data_string}")

        self.database.push(dict(method = "post",
                                path = self.path,
                                query = urlparse(self.path).query,
                                body = self.data_string))
        # Some custom HTML code, possibly generated by another function
        html = ""

        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(html, "utf8"))

        return

class HttpServer:
    def __init__(self, host, port, database):
        self.database = database
        self.host = host
        self.port = port
        return
    def __run(self):
        print(f"Starting the HTTP server @{self.host}:{self.port}")
        # Create an object of the above class
        handler_object = partial(MyHttpRequestHandler, self.database)

        my_server = socketserver.TCPServer((self.host, self.port), handler_object)

        # Star the server
        print("HTTP server started.")
        my_server.serve_forever()
    def start(self):
        x = threading.Thread(target=self.__run)
        return x.start()
