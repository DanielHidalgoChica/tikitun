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
    # TODO: SELECT * FROM CONVERSACION WHERE username_comprador = ? OR username_vendedor = ?
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
