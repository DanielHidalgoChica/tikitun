"""
Repositorio de acceso a datos de conversaciones.
Responsable: Aitor de la Iglesia

Operaciones sobre la tabla CONVERSACION.
"""


def get_conversaciones_usuario(cn, username: str) -> list[dict]:
    """Obtiene todas las conversaciones del usuario.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
    
    Returns:
        Lista de conversaciones (como comprador o vendedor)
    """
    print("   [REPO conversaciones] get_conversaciones_usuario()", username)

    sql = """
        SELECT 
        c.id_chat,
        c.id_producto,
        c.username        AS comprador,
        p.username        AS vendedor,
        p.titulo,
        c.archivado
        FROM Chat c JOIN Producto p ON c.id_producto = p.id_producto 
        WHERE c.username = {username} or p.username = {username}
        ORDER BY c.archivado asc;
        """.format(username=username)
    return []


def set_archivada(cn, id_producto: int, archivada: bool) -> None:
    """Marca una conversación como archivada.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto de la conversación
        archivada: True para archivar
    """
    print("   [REPO conversaciones] set_archivada()", id_producto, archivada)
    # TODO: UPDATE CONVERSACION SET archivada = ? WHERE id_producto = ?
    pass
