"""
Repositorio de acceso a datos de favoritos.
Responsable: Daniel Hidalgo

Operaciones CRUD sobre la tabla FAVORITO.
"""


def add_favorito(cn, username: str, id_producto: int) -> None:
    """Agrega un producto a favoritos.
    
    Esquema: INSERT INTO Favorito (id_producto, username) VALUES (?, ?)
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        id_producto: Producto
    """
    print("   [REPO favoritos] add_favorito()", username, id_producto)
    
    cur = cn.cursor()
    cur.execute("INSERT INTO favorito (id_producto, username) VALUES (?, ?)", 
                (id_producto, username))
    cur.close()


def remove_favorito(cn, username: str, id_producto: int) -> None:
    """Elimina un producto de favoritos.
    
    Esquema: DELETE FROM Favorito WHERE id_producto = ? AND username = ?
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        id_producto: Producto
    """
    print("   [REPO favoritos] remove_favorito()", username, id_producto)
    
    cur = cn.cursor()
    cur.execute("DELETE FROM favorito WHERE id_producto = ? AND username = ?", 
                (id_producto, username))
    cur.close()


def is_favorito(cn, username: str, id_producto: int) -> bool:
    """Verifica si un producto está en favoritos.
    
    Esquema: SELECT COUNT(*) FROM Favorito WHERE username = ? AND id_producto = ?
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        id_producto: Producto
    
    Returns:
        True si está en favoritos
    """
    print("   [REPO favoritos] is_favorito()", username, id_producto)
    
    cur = cn.cursor()
    cur.execute("SELECT COUNT(*) FROM favorito WHERE username = ? AND id_producto = ?", 
                (username, id_producto))
    count = cur.fetchone()[0]
    cur.close()
    
    return count > 0


def get_favoritos(cn, username: str) -> list[dict]:
    """Obtiene todos los productos favoritos del usuario.
    
    Solo devuelve productos que estén disponibles (disponible = 1).
    
    Esquema basado en init.sql:
    - Favorito: id_producto, username
    - Producto: id_producto, username (vendedor), nombre_categoria, titulo,
                descripcion, precio, imagen, promocion, disponible
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
    
    Returns:
        Lista de productos con detalles (id_producto, titulo, precio, 
        descripcion, username_vendedor, imagen, nombre_categoria, promocion)
    """
    print("   [REPO favoritos] get_favoritos()", username)
    
    cur = cn.cursor()
    cur.execute("""
        SELECT p.id_producto, p.titulo, p.precio, p.descripcion,
               p.username AS username_vendedor, p.nombre_categoria, 
               p.imagen, p.promocion, p.disponible
        FROM favorito f
        JOIN producto p ON f.id_producto = p.id_producto
        WHERE f.username = ? AND p.disponible = 1
        ORDER BY p.id_producto DESC
    """, (username,))
    
    # Convertir resultados a lista de dicts
    cols = [desc[0].lower() for desc in cur.description] if cur.description else []
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    cur.close()
    
    return rows
