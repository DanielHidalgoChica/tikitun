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
    # TODO: INSERT INTO CONTRAOFERTA (...) VALUES (...)
    pass


def get_contraofertas(cn, id_producto: int) -> list[dict]:
    """Obtiene todas las contraofertas de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
    
    Returns:
        Lista de contraofertas
    """
    print("   [REPO ventas] get_contraofertas()", id_producto)
    # TODO: SELECT * FROM CONTRAOFERTA WHERE id_producto = ?
    return []


def delete_contraoferta(cn, id_producto: int, username_comprador: str) -> None:
    """Elimina una contraoferta específica.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador de la contraoferta
    """
    print("   [REPO ventas] delete_contraoferta()", id_producto, username_comprador)
    # TODO: DELETE FROM CONTRAOFERTA WHERE id_producto = ? AND username_comprador = ?
    pass
