"""
Servicios de gestión de favoritos.
Responsable: Daniel Hidalgo

Requisitos Funcionales implementados:
- RF3.2: Marcar un producto como favorito
- RF3.3: Quitar un producto de favoritos
- RF3.4: Consultar los favoritos
"""

from src.db.db_app import savepoint
from src.repositories.feed_busqueda_favs import favoritos_repo
from src.repositories.productos import productos_repo


def agregar_favorito(cn, username: str, id_producto: int) -> None:
    """RF3.2: Marca un producto como favorito del usuario.
    
    RS aplicadas:
    - RS3.2.1: El producto debe existir
    - RS3.2.2: El producto debe estar disponible
    - Usuario no puede marcar sus propios productos
    - No duplicar favoritos
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario que marca favorito
        id_producto: Producto a marcar
    
    Raises:
        ValueError: Si producto no existe, no disponible, o ya en favoritos
    """
    print(" [SERVICE favoritos] agregar_favorito()")
    
    # Validar que el producto existe
    producto = productos_repo.get_producto(cn, id_producto)
    if not producto:
        raise ValueError("El producto no existe")
    
    # RS: Solo productos disponibles
    if not producto.get("disponible", False):
        raise ValueError("El producto no está disponible")
    
    # RS: No puede ser tu propio producto
    if producto.get("username_vendedor") == username:
        raise ValueError("No puedes marcar tus propios productos como favoritos")
    
    # RS: No duplicar favoritos
    if favoritos_repo.is_favorito(cn, username, id_producto):
        raise ValueError("El producto ya está en favoritos")
    
    savepoint(cn, "SP_ADD_FAVORITO")
    favoritos_repo.add_favorito(cn, username, id_producto)


def quitar_favorito(cn, username: str, id_producto: int) -> None:
    """RF3.3: Elimina un producto de favoritos del usuario.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        id_producto: Producto a quitar
    
    Raises:
        ValueError: Si el producto no está en favoritos
    """
    print(" [SERVICE favoritos] quitar_favorito()")
    
    if not favoritos_repo.is_favorito(cn, username, id_producto):
        raise ValueError("El producto no está en favoritos")
    
    savepoint(cn, "SP_REMOVE_FAVORITO")
    favoritos_repo.remove_favorito(cn, username, id_producto)


def consultar_favoritos(cn, username: str) -> list[dict]:
    """RF3.4: Obtiene todos los productos favoritos del usuario.
    
    Solo devuelve productos que sigan disponibles.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
    
    Returns:
        Lista de productos favoritos con sus detalles
    """
    print(" [SERVICE favoritos] consultar_favoritos()")
    return favoritos_repo.get_favoritos(cn, username)
