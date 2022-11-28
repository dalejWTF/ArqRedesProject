from http.server import HTTPServer, BaseHTTPRequestHandler
import time

HOST = "192.168.68.114"
PORT = 9999
HTML_TEMPLATE = """

<!DOCTYPE html>
<html>
<meta charset="UTF-8">
<head>
  <title>Proyecto de Redes</title>
</head>
<body>
    <h1>Arquitectura y Seguridad de Redes</h1>
    <h3>Proyecto HTTP Server</h3>
    <p>Solicita: {}</p>
    <header>
        <h1>Integrantes</h1>
        <h4>Daniel Ulloa</h4>
        <h4>José Romero</h4>
        <h4>Roberto </h4> 
    </header>
    
</body>
</html>

"""
class RedesHttpServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(bytes(HTML_TEMPLATE.format(self.path), "UTF-8"))
    
    def do_POST(self):
        response="""
        ["date": {},
        "request": {}
        ]
        """
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        date = time.strftime("%Y - %m - %d %H:%M:%S",time.localtime(time.time()))
        self.wfile.write(bytes(response.format(date,self.path), "UTF-8"))


if __name__ == "__main__":   
    server = HTTPServer((HOST, PORT),RedesHttpServer)
    try:
        print("Running server...")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Server stopped.")