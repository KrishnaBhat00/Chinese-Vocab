from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import Vocab
import time
from pytreemap import TreeMap

hostName = "localhost"
serverPort = 8080

vocabs = TreeMap(comparator=None)
vocabs[0] = Vocab.Vocab("周围", "zhōuwéi", "around")


def getNext():
    if True:
        return vocabs[0].getChars()


class Server(BaseHTTPRequestHandler):
    title = "<title>Chinese Review Site</title>"
    meta = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8 />"'
    script = ""
    form = '<form method="get" action="/">'
    form += '<button name="next" value="Next" type="submit">Next</button>'
    form += "</form>"

    def do_GET(self):
        display = ""
        query = urlparse(self.path).query
        param  = ""
        if query.find("=") > -1: 
            queryComponents = dict(qc.split('=') for qc in query.split('&'))
            if ('next' in queryComponents):
                param = queryComponents["next"]
                display = getNext()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"<html><head>\n{self.title}\n{self.meta}", "utf-8"))
        self.wfile.write(bytes(self.script, "utf-8"))
        self.wfile.write(bytes("</head>", "utf-8"))
        self.wfile.write(bytes(f"<p>Request: {self.path}</p>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This site is for reviewing Chinese.</p>", "utf-8"))
        self.wfile.write(bytes('<p>', 'utf-8'))
        self.wfile.write(bytes("这个网站是给你中文学习。", 'utf-8'))
        self.wfile.write(bytes("</p></meta>", "utf-8"))
        self.wfile.write(bytes(self.form, "utf-8"))
        self.wfile.write(bytes(display, "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
        webServer = HTTPServer((hostName, serverPort), Server)
        print("Server started http://%s:%s" % (hostName, serverPort))
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass
        
        webServer.server_close()
        print("server stopped")