"""
Repositorio de acceso a datos de ventas.
Responsable: Juan Manuel Fernández

Operaciones CRUD sobre la tabla VENTA.
"""


def insert_venta(cn, venta: dict) -> None:
    """Inserta un registro de venta.
    
    Args:
        cn: Conexión a la base de datos
        venta: Dict con id_producto, username_comprador, recepcion_confirmada
               precio_final, valoracion
    """
    print("   [REPO ventas] insert_venta()", venta)

    cur = cn.cursor()
    cur.execute("INSERT INTO VENDIDO VALUES (?,?,?,?,?)", (venta['id_producto'],
                venta['username'], venta['recepcion_confirmada'], venta['precio_final'], venta['valoracion']))
    cur.close()

    pass


def get_venta(cn, id_producto: int) -> dict | None:
    """Obtiene una venta por producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto vendido
    
    Returns:
        Dict con datos de la venta o None
    """
    print("   [REPO ventas] get_venta()", id_producto)

    cur = cn.cursor()
    cur.execute("SELECT * FROM VENDIDO WHERE id_producto = ?", id_producto)

    # Convertir resultado a diccionario
    cols = [desc[0].lower() for desc in cur.description] if cur.description else []
    venta = dict(zip(cols, cur.fetchone()))

    cur.close()

    return venta


def update_estado_recepcion(cn, id_producto: int, recibido: int) -> None:
    """Actualiza el estado de recepción de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        recibido: 1 si ya fue recibido, 0 si no
    """
    print("   [REPO ventas] update_estado_recepcion()", id_producto, recibido)
    
    cur = cn.cursor()
    cur.execute("UPDATE VENDIDO SET estado_recepcion = ? WHERE id_producto = ?", (recibido, id_producto))
    cur.close()

def update_puntuacion_venta(cn, id_producto: int, puntuacion : float) -> None:
    """Actualiza la puntuación de una venta
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username: Comprador
        puntuacion: Puntuación (0, 0.5, 1, ..., 5)
    """
    print("   [REPO ventas] update_puntuacion_venta()", id_producto, puntuacion)
    
    cur = cn.cursor()
    cur.execute("UPDATE VENDIDO SET valoracion = ? WHERE id_producto = ?", (puntuacion, id_producto))
    cur.close()

def get_ventas_usuario(cn, username : str) -> list[dict]:
    """Devuelve todas las ventas asociadas a productos del usuario.

    Args:
        cn: Conexión a la base de datos
        username: Comprador
    
    Returns:
        Lista de ventas
    """
    print("   [REPO ventas] get_ventas_usuario()", username)

    cur = cn.cursor()
    cur.execute("SELECT * FROM VENDIDO WHERE id_producto IN (SELECT id_producto FROM PRODUCTO WHERE username = ?)",
                username)

    # Convertir resultados a lista de dicts
    cols = [desc[0].lower() for desc in cur.description] if cur.description else []
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]

    cur.close()

    return rows