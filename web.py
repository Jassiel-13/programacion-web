from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import os

class WebRequestHandler(BaseHTTPRequestHandler):
    CONTENTS = {
        '/proyecto/web-uno': "<html><h1>Proyecto: web-uno</h1></html>",
        '/proyecto/web-dos': "<html><h1>Proyecto: web-dos</h1></html>",
        '/proyecto/web-tres': "<html><h1>Proyecto: web-tres</h1></html>",
    }

    # Contenido de home.html directamente en el código
    HOME_PAGE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home Page</title>
    </head>
    <body>
        <h1>Home Page</h1>
        <ul>
            <li><a href="/proyecto/web-uno">Proyecto Web Uno</a></li>
            <li><a href="/proyecto/web-dos">Proyecto Web Dos</a></li>
            <li><a href="/proyecto/web-tres">Proyecto Web Tres</a></li>
            <li><a href="/1.html">Enlace a 1.html</a></li>
            <li><a href="/personal-page">Ana Lee</a></li>
        </ul>
    </body>
    </html>
    """

    # Contenido de la página personalizada
    PERSONAL_PAGE = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Ana Lee</title>
        <link href="css/style.css" rel="stylesheet">
    </head>
    <body>
        <h1>Ana Lee</h1> 
        <h2>Desarrolladora Web (Música/Diseño/Empresaria)</h2>
        <small>Este texto fue generado por Copilot:</small>
        <h3>
            ¡Hola! Soy Ana Lee, una desarrolladora web que se especializa en la
            creación de sitios web y aplicaciones web. Me encanta trabajar con
            tecnologías web modernas y crear experiencias de usuario atractivas y
            fáciles de usar. También soy una artista y empresaria apasionada, y me
            encanta combinar mi creatividad y mi pasión por la tecnología para crear
            soluciones web únicas y efectivas.
        </h3>
        <br>
        <h2>Proyectos</h2>
        <h3><a href="/proyecto/1"> Web Estática - App de recomendación de libros </a></h3>
        <h3><a href="/proyecto/2"> Web App - MeFalta, qué película o serie me falta ver </a></h3>
        <h3><a href="/proyecto/3"> Web App - Foto22, web para gestión de fotos </a></h3>
        <br>
        <h2>Experiencia</h2>
        <h3>Desarrolladora Web Freelance</h3>
        <h3>Backend: FastAPI, nodejs, Go</h3>
        <h3>Frontend: JavaScript, htmx, React</h3>
    </body>
    </html>
    """

    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        # Registro de la petición
        host_header = self.headers.get('Host')
        user_agent_header = self.headers.get('User-Agent')
        requested_path = self.path

        # Generar la respuesta HTML basado en el contenido en memoria o archivos
        response_message = self.get_response()

        # Enviar respuesta
        status_code = 200 if self.path in self.CONTENTS or self.path.endswith('.html') else 404
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Server", "Python HTTP Server")
        self.send_header("Date", self.date_time_string())
        self.end_headers()
        self.wfile.write(response_message.encode("utf-8"))

        # Imprimir información en la consola
        print(f"Request:")
        print(f"  Host: {host_header}")
        print(f"  User-Agent: {user_agent_header}")
        print(f"  Requested Path: {requested_path}")
        print(f"Response:")
        print(f"  Content-Type: text/html")
        print(f"  Server: Python HTTP Server")
        print(f"  Date: {self.date_time_string()}")

    def do_POST(self):
        # Respuesta para peticiones POST
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Server", "Python HTTP Server")
        self.send_header("Date", self.date_time_string())
        self.end_headers()
        self.wfile.write(b"POST request received!")

    def get_response(self):
        if self.path == '/':
            # Sirve el contenido de HOME_PAGE en la ruta principal
            return self.HOME_PAGE

        # Sirve archivos HTML estáticos como 1.html
        elif self.path.endswith('.html'):
            try:
                with open(self.path[1:], 'r') as file:  # remove leading '/'
                    return file.read()
            except FileNotFoundError:
                return "<h1>Error 404: Not Found</h1>"

        # Sirve contenido HTML dinámico desde el diccionario
        elif self.path.startswith('/proyecto/'):
            return self.CONTENTS.get(self.path, "<h1>Error 404: Not Found</h1>")

        # Maneja la página personalizada si se solicita
        elif self.path == '/personal-page':
            return self.PERSONAL_PAGE
        
        # Maneja rutas no definidas
        return "<h1>Error 404: Not Found</h1>"

if __name__ == "__main__":
    print("Starting server on port 8000")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
