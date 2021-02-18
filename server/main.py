# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import glob
from importlib import import_module
import sys

hostName = "0.0.0.0"
serverPort = 8080


def get_modules():
    base_path = os.path.dirname(__file__)
    files = [f for f in glob.glob(base_path + "/lib/*.py")]

    processed_files = []

    for name in files:
        if "lib/__init__.py" in name:
            continue
        f = name.replace(".py", "").replace("lib/", "").replace(base_path+"/", "")
        processed_files.append(f)

    return processed_files


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        route = self.path.replace("/", "", 1)
        if route in get_modules():
            mod = import_module("lib." + route)
            result = mod.run_command()

            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            self.wfile.write(result)

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"{route} not found", "utf-8"))


def main():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":        
    main()