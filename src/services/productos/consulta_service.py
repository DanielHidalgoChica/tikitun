"""
Servicios de consulta de productos.
Responsable: Roberto González

Requisitos Funcionales implementados:
- RF2.4: Consultar producto (detalles completos)
"""

from src.repositories.productos import productos_repo


def consultar_producto(cn, id_producto: int) -> dict:
    """RF2.4: Obtiene información detallada de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
    
    Returns:
        Dict con título, descripción, precio, categoría, imagen,
        username_vendedor, valoración_vendedor, disponible, etc.
    
    Raises:
        ValueError: Si el producto no existe
    """
    print(" [SERVICE productos] consultar_producto()")
    
    producto = productos_repo.get_producto(cn, id_producto)
    
    if not producto:
        raise ValueError("El producto no existe.")
    
    return producto
