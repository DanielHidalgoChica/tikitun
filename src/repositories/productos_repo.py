def insert_producto(cn, producto: dict) -> int:
    print("   [REPO productos] insert_producto()", producto)
    # TODO: INSERT INTO Producto (...) VALUES (...)
    return 1  # id fake

def search_productos(cn, filtros: dict) -> list[dict]:
    print("   [REPO productos] search_productos()", filtros)
    # TODO: SELECT ... FROM Producto WHERE ...
    return [
        {"id_producto": 1, "titulo": "Guitarra", "precio": 120, "vendedor": "ana"},
        {"id_producto": 2, "titulo": "Bajo", "precio": 200, "vendedor": "paco"},
    ]
