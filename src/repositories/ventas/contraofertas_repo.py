"""
Repositorio de acceso a datos de contraofertas.
Responsable: Juan Manuel Fernández

Operaciones CRUD sobre la tabla CONTRAOFERTA.
"""


def insert_contraoferta(cn, contraoferta: dict) -> None:
    """Inserta una contraoferta.
    
    Args:
        cn: Conexión a la base de datos
        contraoferta: Dict con id_producto, username_comprador, precio_oferta
    """
    print("   [REPO ventas] insert_contraoferta()", contraoferta)
    
    cur = cn.cursor()
    cur.execute("INSERT INTO CONTRAOFERTA VALUES (?,?,?)", (contraoferta['id_producto'],
                contraoferta['username'], contraoferta['precio']))
    cur.close()


def get_contraofertas(cn, id_producto: int) -> list[dict]:
    """Obtiene todas las contraofertas de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
    
    Returns:
        Lista de contraofertas
    """
    print("   [REPO ventas] get_contraofertas()", id_producto)

    cur = cn.cursor()
    cur.execute("SELECT * FROM CONTRAOFERTA WHERE id_producto = ?", id_producto)

    # Convertir resultados a lista de dicts
    cols = [desc[0].lower() for desc in cur.description] if cur.description else []
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]

    cur.close()

    return rows

def get_contraoferta(cn, id_producto: int, id_usuario : str) -> dict:
    """Obtiene la contraoferta asociada a un producto que haya sido realizada por ese usuario
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
    
    Returns:
        Lista de contraofertas
    """
    print("   [REPO ventas] get_contraoferta()", id_producto, id_usuario)

    cur = cn.cursor()
    cur.execute("SELECT * FROM CONTRAOFERTA WHERE id_producto = ? AND username = ?", (id_producto, id_usuario))

    # Convertir resultado a diccionario
    cols = [desc[0].lower() for desc in cur.description] if cur.description else []
    contraoferta = dict(zip(cols, cur.fetchone()))
    cur.close()

    return contraoferta

def delete_contraoferta(cn, id_producto: int, username_comprador: str) -> None:
    """Elimina una contraoferta específica.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador de la contraoferta
    """
    print("   [REPO ventas] delete_contraoferta()", id_producto, username_comprador)
    # TODO: DELETE FROM CONTRAOFERTA WHERE id_producto = ? AND username_comprador = ?

    cur = cn.cursor()
    cur.execute("DELETE FROM CONTRAOFERTA WHERE id_producto = ? AND username_comprador = ?",
                (id_producto, username_comprador))
    cur.close()

    pass
