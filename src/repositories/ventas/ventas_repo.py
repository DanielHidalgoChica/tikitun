"""
Repositorio de acceso a datos de ventas.
Responsable: Juan Manuel Fernández

Operaciones CRUD sobre la tabla VENTA.
"""


def insert_venta(cn, venta: dict) -> None:
    """Inserta un registro de venta.
    
    Args:
        cn: Conexión a la base de datos
        venta: Dict con id_producto, username_comprador, username_vendedor,
               precio_final, fecha_venta, estado_recepcion
    """
    print("   [REPO ventas] insert_venta()", venta)
    # TODO: INSERT INTO VENTA (...) VALUES (...)
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
    # TODO: SELECT * FROM VENTA WHERE id_producto = ?
    return None


def update_estado_recepcion(cn, id_producto: int, recibido: bool) -> None:
    """Actualiza el estado de recepción de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        recibido: True si ya fue recibido
    """
    print("   [REPO ventas] update_estado_recepcion()", id_producto, recibido)
    # TODO: UPDATE VENTA SET estado_recepcion = ? WHERE id_producto = ?
    pass
