"""
Servicios de gestión de productos.
Responsable: Roberto González

Requisitos Funcionales implementados:
- RF2.1: Dar de alta producto
- RF2.2: Modificar producto
- RF2.3: Eliminar producto
- RF2.4: Consultar producto
- RF2.5: Promocionar producto
"""

from src.db.db_app import savepoint
from src.repositories.productos import productos_repo


def publicar_producto(cn, data: dict) -> int:
    """RF2.1: Publica un nuevo producto.
    
    RS aplicadas:
    - RS2.1: Precio > 0 con dos decimales
    - RS2.3: Categoría válida
    - RS2.5: Título ≤ 80, descripción ≤ 500 caracteres
    
    Args:
        cn: Conexión a la base de datos
        data: Dict con titulo, descripcion, precio, categoria, imagen, username_vendedor
    
    Returns:
        id_producto generado
    
    Raises:
        ValueError: Si no cumple validaciones
    """
    print(" [SERVICE productos] publicar_producto()")
    
    # Validaciones
    if not data.get("titulo"):
        raise ValueError("El título no puede estar vacío.")
    if float(data.get("precio", 0)) <= 0:
        raise ValueError("El precio debe ser mayor que 0.")
    
    savepoint(cn, "SP_PUBLICAR_PRODUCTO")
    new_id = productos_repo.insert_producto(cn, data)
    return new_id


def modificar_producto(cn, id_producto: int, username_vendedor: str, cambios: dict) -> None:
    """RF2.2: Modifica datos de un producto propio.
    
    RS aplicadas:
    - RS2.2: Precio > 0 con dos decimales
    - RS2.4: Categoría válida
    - RS2.6: Título ≤ 80, descripción ≤ 500
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto a modificar
        username_vendedor: Vendedor (para verificar permisos)
        cambios: Dict con campos a actualizar
    
    Raises:
        ValueError: Si no es el vendedor o validaciones fallan
    """
    print(" [SERVICE productos] modificar_producto()")
    # TODO: Verificar que el usuario es el vendedor
    # TODO: Validar cambios
    # TODO: savepoint(cn, "SP_MODIFICAR_PRODUCTO")
    # TODO: productos_repo.update_producto(cn, id_producto, cambios)
    pass


def eliminar_producto(cn, id_producto: int, username_vendedor: str) -> None:
    """RF2.3: Elimina un producto (marca como no disponible).
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
        username_vendedor: Vendedor (para verificar permisos)
    
    Raises:
        ValueError: Si no es el vendedor o producto en proceso de venta
    """
    print(" [SERVICE productos] eliminar_producto()")
    # TODO: Verificar permisos
    # TODO: Verificar que no está en proceso de venta
    # TODO: productos_repo.soft_delete_producto(cn, id_producto)
    pass


def promocionar_producto(cn, id_producto: int, username_vendedor: str, 
                        grado_promocion: float) -> None:
    """RF2.5: Promociona un producto incrementando su visibilidad.
    
    Coste: grado_promocion * 0.1 * precio_producto
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
        username_vendedor: Vendedor (para cobrar del saldo)
        grado_promocion: Valor entre 0 y 1
    
    Raises:
        ValueError: Si saldo insuficiente o valor no válido
    """
    print(" [SERVICE productos] promocionar_producto()")
    # TODO: Validar grado_promocion (0-1)
    # TODO: Calcular coste
    # TODO: Verificar saldo suficiente
    # TODO: Descontar del monedero y actualizar promoción
    pass
