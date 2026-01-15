"""
Servicios de gestión de mensajes.
Responsable: Aitor de la Iglesia

Requisitos Funcionales implementados:
- RF5.1: Enviar mensaje
- RF5.2: Consultar conversación
- RF5.3: Adjuntar archivo
- RF5.4: Buscar mensaje
- RF5.5: Archivar conversación
"""

from src.db.db_app import savepoint
from src.repositories.mensajes import mensajes_repo, conversaciones_repo


def enviar_mensaje(cn, data: dict) -> None:
    """RF5.1: Envía un mensaje en una conversación.
    
    Args:
        cn: Conexión a la base de datos
        data: Dict con id_vendedor, id_comprador, id_producto, emisor, texto
    
    Raises:
        ValueError: Si texto vacío o conversación no existe
    """
    print(" [SERVICE mensajes] enviar_mensaje()")
    # TODO: Validar texto no vacío
    # TODO: savepoint(cn, "SP_ENVIAR_MENSAJE")
    # TODO: mensajes_repo.insert_mensaje(cn, data)
    # TODO: Enviar notificación por correo
    pass


def consultar_conversacion(cn, id_producto: int, username_comprador: str, 
                          username_vendedor: str) -> list[dict]:
    """RF5.2: Obtiene todos los mensajes de una conversación.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador
        username_vendedor: Vendedor
    
    Returns:
        Lista de mensajes ordenados por fecha
    """
    print(" [SERVICE mensajes] consultar_conversacion()")
    # TODO: mensajes_repo.get_mensajes_conversacion(...)
    # TODO: Marcar mensajes como leídos
    return []


def adjuntar_archivo(cn, data: dict) -> None:
    """RF5.3: Adjunta un archivo a un mensaje.
    
    Args:
        cn: Conexión a la base de datos
        data: Dict con id_producto, comprador, vendedor, emisor, archivo
    """
    print(" [SERVICE mensajes] adjuntar_archivo()")
    # TODO: Implementar
    pass


def buscar_mensajes(cn, username: str, filtros: dict) -> list[dict]:
    """RF5.4: Busca mensajes según filtros.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario que busca
        filtros: Dict con palabras_clave, usuario, fecha
    
    Returns:
        Mensajes que coinciden con filtros
    """
    print(" [SERVICE mensajes] buscar_mensajes()")
    return mensajes_repo.search_mensajes(cn, username, filtros)


def archivar_conversacion(cn, id_producto: int) -> None:
    """RF5.5: Archiva una conversación cuando se completa la venta.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto de la conversación
    """
    print(" [SERVICE mensajes] archivar_conversacion()")
    # TODO: conversaciones_repo.set_archivada(cn, id_producto, True)
    pass
