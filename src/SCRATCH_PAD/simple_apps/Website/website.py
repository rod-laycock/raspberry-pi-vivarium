from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    name = "Rosalia"
    return render_template("index.html", title="Welcome", username=name)


if __name__ == "__main__":
    app.run()


# from http.server import BaseHTTPRequestHandler, HTTPServer
# import time

# hostName = "localhost"
# serverPort = 8080

# class MyServer(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
#         self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
#         self.wfile.write(bytes("<body>", "utf-8"))
#         self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
#         self.wfile.write(bytes("</body></html>", "utf-8"))

# if __name__ == "__main__":
#     webServer = HTTPServer((hostName, serverPort), MyServer)
#     print("Server started http://%s:%s" % (hostName, serverPort))

#     try:
#         webServer.serve_forever()
#     except KeyboardInterrupt:
#         pass

#     webServer.server_close()
#     print("Server stopped.")
