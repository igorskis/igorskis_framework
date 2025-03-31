import os

def serve_static_file(path):
    """Функция для обработки статических файлов."""
    # Убираем префикс "/static" из пути
    static_path = os.path.join(os.getcwd(), "static", path[len("/static/"):])
    print(f"Trying to serve static file: {static_path}")  # Выведем путь для отладки
    if os.path.exists(static_path) and os.path.isfile(static_path):
        with open(static_path, "rb") as f:
            return f.read()
    return None
