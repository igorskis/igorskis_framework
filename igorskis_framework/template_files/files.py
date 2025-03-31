manage = '''import time
from watchdog.observers import Observer
from igorskis_framework.restart_handler import RestartHandler

if __name__ == "__main__":
    print("[INFO] Автоперезапуск сервера активирован...")
    event_handler = RestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n[INFO] Остановка сервера.")
        event_handler.server_process.terminate()
        observer.stop()

    observer.join()
'''

server = '''from igorskis_framework.middlewares.static_files import serve_static_file
from wsgiref.simple_server import make_server
from igorskis_framework.router import router
from igorskis_framework.middlewares.cors import CORS
from settings import STATIC_URL
import urls  # Загружаем маршруты

def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    
    # Если путь начинается с /static/, обслуживаем статический файл
    if path.startswith(STATIC_URL):
        file_data = serve_static_file(path)
        if file_data:
            status = "200 OK"
            # Определяем тип контента в зависимости от расширения
            if path.endswith(".css"):
                content_type = "text/css"
            elif path.endswith(".js"):
                content_type = "application/javascript"
            else:
                content_type = "application/octet-stream"
            
            headers = [("Content-Type", content_type), ("Content-Length", str(len(file_data)))]
            start_response(status, headers)
            return [file_data]
        else:
            status = "404 Not Found"
            response_body = b"<h1>File not found</h1>"
            headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]
            start_response(status, headers)
            return [response_body]
    
    # Для обычных маршрутов
    view, params = router.resolve(path)
    
    if view:
        response_body = view(**params).encode("utf-8")
        status = "200 OK"
        headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]
    else:
        response_body = b"<h1>404 Not Found</h1>"
        status = "404 Not Found"
        headers = [("Content-Type", "text/html"), ("Content-Length", str(len(response_body)))]

    start_response(status, headers)
    return [response_body]


app = CORS(application)

if __name__ == "__main__":
    with make_server("", 8000, app) as server:
        print("Serving on port 8000...")
        server.serve_forever()
'''

urls = '''from igorskis_framework.router import router
from views import *

router.add_route("/", index)
'''

views = '''from igorskis_framework.templates import html

def index():
    return html("index.html")
'''

models = '''from igorskis_framework.models import Model'''
settings = '''STATIC_URL = "/static/"'''

init = ''''''

index_html = '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
        <link rel="icon" href="/static/logo.svg">
        <link rel="stylesheet" href="/static/style.css">
        <title>Welcome to Igorskis Framework!</title>
    </head>
    <body>
        <h1>Welcome to Igorskis Framework!</h1>
        <p>This is a web framework for creating web applications.</p>
        <p>The installation has been completed successfully!</p>
        <p>You can now start creating your web applications.</p>
        <a href="https://pypi.org/project/igorskis-framework/" target="_blank"><svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="white"/>
            <text x="40" y="120" font-size="100" fill="red" font-family="Arial">I</text>
            <text x="100" y="120" font-size="100" fill="red" font-family="Arial">F</text>
        </svg>
        </a>
    </body>
</html>
'''

style_css = '''body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 20px;
}

h1 {
    color: #157444;
}

a {
    text-decoration: none;
}

svg:hover {
    transform: scale(1.2);
}
'''

logo = '''<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="white"/>
        <text x="40" y="120" font-size="100" fill="red" font-family="Arial">I</text>
        <text x="100" y="120" font-size="100" fill="red" font-family="Arial">F</text>
    </svg>'''