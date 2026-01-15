"""
Repositorio de acceso a datos de productos.
Responsable: Roberto González

Operaciones CRUD sobre la tabla PRODUCTO.
"""


def insert_producto(cn, producto: dict) -> int:
    """Inserta un nuevo producto en la BD.
    
    Args:
        cn: Conexión a la base de datos
        producto: Dict con titulo, descripcion, precio, categoria, imagen, username_vendedor
    
    Returns:
        id_producto generado
    """
    print("   [REPO productos] insert_producto()", producto)
    # TODO: INSERT INTO PRODUCTO (...) VALUES (...) RETURNING id_producto
    return 1  # ID fake


def get_producto(cn, id_producto: int) -> dict | None:
    """Obtiene un producto por ID.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
    
    Returns:
        Dict con datos del producto o None si no existe
    """
    print("   [REPO productos] get_producto()", id_producto)
    # TODO: SELECT * FROM PRODUCTO WHERE id_producto = ?
    
    # Demo (eliminar cuando implementes)
    return {
        "id_producto": id_producto,
        "titulo": "Producto Demo",
        "precio": 99.99,
        "disponible": True,
        "username_vendedor": "vendedor_demo"
    }


def update_producto(cn, id_producto: int, cambios: dict) -> None:
    """Actualiza campos de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
        cambios: Dict con campos a modificar
    """
    print("   [REPO productos] update_producto()", id_producto, cambios)
    # TODO: UPDATE PRODUCTO SET ... WHERE id_producto = ?
    pass


def soft_delete_producto(cn, id_producto: int) -> None:
    """Marca un producto como no disponible.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
    """
    print("   [REPO productos] soft_delete_producto()", id_producto)
    # TODO: UPDATE PRODUCTO SET disponible = false WHERE id_producto = ?
    pass


def search_productos(cn, filtros: dict) -> list[dict]:
    """Busca productos según filtros.
    
    Args:
        cn: Conexión a la base de datos
        filtros: Dict con q (query), categoria, orden, etc.
    
    Returns:
        Lista de productos que coinciden
    """
    print("   [REPO productos] search_productos()", filtros)
    # TODO: SELECT * FROM PRODUCTO WHERE disponible = true AND ...
    
    # Demo (eliminar cuando implementes)
    return [
        {"id_producto": 1, "titulo": "Producto 1", "precio": 29.99},
        {"id_producto": 2, "titulo": "Producto 2", "precio": 49.99},
    ]
