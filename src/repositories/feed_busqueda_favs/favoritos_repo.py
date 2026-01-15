"""
Repositorio de acceso a datos de favoritos.
Responsable: Daniel Hidalgo

Operaciones CRUD sobre la tabla FAVORITO.
"""


def add_favorito(cn, username: str, id_producto: int) -> None:
    """Agrega un producto a favoritos.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        id_producto: Producto
    """
    print("   [REPO favoritos] add_favorito()", username, id_producto)
    # TODO: INSERT INTO FAVORITO (id_producto, username) VALUES (?, ?)
    pass


def remove_favorito(cn, username: str, id_producto: int) -> None:
    """Elimina un producto de favoritos.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        id_producto: Producto
    """
    print("   [REPO favoritos] remove_favorito()", username, id_producto)
    # TODO: DELETE FROM FAVORITO WHERE id_producto = ? AND username = ?
    pass


def is_favorito(cn, username: str, id_producto: int) -> bool:
    """Verifica si un producto está en favoritos.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        id_producto: Producto
    
    Returns:
        True si está en favoritos
    """
    print("   [REPO favoritos] is_favorito()", username, id_producto)
    # TODO: SELECT COUNT(*) FROM FAVORITO WHERE username = ? AND id_producto = ?
    return False  # Demo


def get_favoritos(cn, username: str) -> list[dict]:
    """Obtiene todos los productos favoritos del usuario.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
    
    Returns:
        Lista de productos con detalles
    """
    print("   [REPO favoritos] get_favoritos()", username)
    # TODO: 
    # SELECT P.* FROM FAVORITO F
    # JOIN PRODUCTO P ON F.id_producto = P.id_producto
    # WHERE F.username = ? AND P.disponible = true
    # ORDER BY F.fecha_marcado DESC (si tienes ese campo)
    return []  # Demo
