from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from Reader import vocabs
import time
from pytreemap import TreeMap

hostName = "localhost"
serverPort = 8080



class Server(BaseHTTPRequestHandler):
    title = "<title>Chinese Review Site</title>"
    meta = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'
    script = '<script language="JavaScript">\nalert();\nreveal = true;\ndef getNext() {\n'
    script += f'\talert();\n\tdocument.getElementById("char").innerHTML = "red";'
    script += '\n}\n</script>\n'
    form = '<button id="next" onclick=getNext()>Next</button>\n'

    reveal = True

    def getNext(self):
        if self.reveal == True:
            self.reveal = False
            return vocabs[0].getChars()
        else:
            self.reveal = True
            return f"{vocabs[0].getPinyin}\t{vocabs[0].getDefin}"


    def do_GET(self):
        display = ""
        query = urlparse(self.path).query
        param  = ""
        if query.find("=") > -1: 
            queryComponents = dict(qc.split('=') for qc in query.split('&'))
            if ('next' in queryComponents):
                param = queryComponents["next"]
                display = self.getNext()
                self.reveal != self.reveal

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"<html>\n<head>\n{self.title}\n{self.meta}", "utf-8"))
        self.wfile.write(bytes(self.script, "utf-8"))
        self.wfile.write(bytes("</head>\n", "utf-8"))
        self.wfile.write(bytes(f"<p>Request: {self.path}</p>\n", "utf-8"))
        self.wfile.write(bytes("<body>\n", "utf-8"))
        self.wfile.write(bytes("<p>This site is for reviewing Chinese.</p>\n", "utf-8"))
        self.wfile.write(bytes('<p>', 'utf-8'))
        self.wfile.write(bytes("这个网站是给你中文学习。", 'utf-8'))
        self.wfile.write(bytes("</p>\n</meta>\n", "utf-8"))
        self.wfile.write(bytes(self.form, "utf-8"))
        self.wfile.write(bytes("<span id='char'></span>\n", "utf-8"))
        self.wfile.write(bytes(display, "utf-8"))
        self.wfile.write(bytes("</body>\n</html>", "utf-8"))

if __name__ == "__main__":
        webServer = HTTPServer((hostName, serverPort), Server)
        print("Server started http://%s:%s" % (hostName, serverPort))
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass
        
        webServer.server_close()
        print("server stopped")