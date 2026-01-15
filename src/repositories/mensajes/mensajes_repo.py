"""
Repositorio de acceso a datos de mensajes.
Responsable: Aitor de la Iglesia

Operaciones CRUD sobre la tabla MENSAJE.
"""


def insert_mensaje(cn, mensaje: dict) -> None:
    """Inserta un nuevo mensaje.
    
    Args:
        cn: Conexión a la base de datos
        mensaje: Dict con todos los campos del mensaje
    """
    print("   [REPO mensajes] insert_mensaje()", mensaje)
    # TODO: INSERT INTO MENSAJE (...) VALUES (...)
    pass


def get_mensajes_conversacion(cn, id_producto: int, username_comprador: str,
                              username_vendedor: str) -> list[dict]:
    """Obtiene todos los mensajes de una conversación.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador
        username_vendedor: Vendedor
    
    Returns:
        Lista de mensajes ordenados por fecha
    """
    print("   [REPO mensajes] get_mensajes_conversacion()")
    # TODO: SELECT * FROM MENSAJE WHERE ... ORDER BY fecha_envio
    return []


def mark_as_read(cn, mensaje_ids: list[int]) -> None:
    """Marca mensajes como leídos.
    
    Args:
        cn: Conexión a la base de datos
        mensaje_ids: IDs de mensajes
    """
    print("   [REPO mensajes] mark_as_read()", mensaje_ids)
    # TODO: UPDATE MENSAJE SET leido = true WHERE id_mensaje IN (...)
    pass


def search_mensajes(cn, username: str, filtros: dict) -> list[dict]:
    """Busca mensajes según filtros.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        filtros: Dict con palabras_clave, usuario, fecha
    
    Returns:
        Mensajes que coinciden
    """
    print("   [REPO mensajes] search_mensajes()", username, filtros)
    # TODO: SELECT con WHERE y LIKE para búsqueda
    return []
