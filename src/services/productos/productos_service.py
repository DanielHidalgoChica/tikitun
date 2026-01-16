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


# Constantes de validación
MAX_TITULO_LENGTH = 80
MAX_DESCRIPCION_LENGTH = 500


def publicar_producto(cn, data: dict) -> int:
    """RF2.1: Publica un nuevo producto.
    
    RS aplicadas:
    - RS2.1: Precio > 0 con dos decimales
    - RS2.3: Categoría válida (debe existir en BD)
    - RS2.5: Título ≤ 80, descripción ≤ 500 caracteres
    
    Args:
        cn: Conexión a la base de datos
        data: Dict con:
            - titulo: str (obligatorio, max 80 chars)
            - descripcion: str (opcional, max 500 chars)
            - precio: float (obligatorio, > 0)
            - nombre_categoria: str (obligatorio, debe existir)
            - imagen: bytes (opcional)
            - username_vendedor: str (obligatorio)
    
    Returns:
        id_producto generado
    
    Raises:
        ValueError: Si no cumple validaciones
    """
    # --- Validaciones ---
    
    # Título obligatorio y longitud máxima (RS2.5)
    titulo = data.get("titulo", "").strip()
    if not titulo:
        raise ValueError("El título es obligatorio.")
    if len(titulo) > MAX_TITULO_LENGTH:
        raise ValueError(f"El título no puede superar {MAX_TITULO_LENGTH} caracteres.")
    
    # Descripción longitud máxima (RS2.5)
    descripcion = data.get("descripcion", "").strip()
    if len(descripcion) > MAX_DESCRIPCION_LENGTH:
        raise ValueError(f"La descripción no puede superar {MAX_DESCRIPCION_LENGTH} caracteres.")
    
    # Precio > 0 (RS2.1)
    try:
        precio = float(data.get("precio", 0))
    except (TypeError, ValueError):
        raise ValueError("El precio debe ser un número válido.")
    
    if precio <= 0:
        raise ValueError("El precio debe ser mayor que 0.")
    
    # Redondear a 2 decimales
    precio = round(precio, 2)
    
    # Categoría obligatoria y válida (RS2.3)
    nombre_categoria = data.get("nombre_categoria", "").strip()
    if not nombre_categoria:
        raise ValueError("Debe seleccionar una categoría.")
    
    if not productos_repo.categoria_existe(cn, nombre_categoria):
        raise ValueError(f"La categoría '{nombre_categoria}' no es válida.")
    
    # Username vendedor obligatorio
    username_vendedor = data.get("username_vendedor", "").strip()
    if not username_vendedor:
        raise ValueError("El vendedor es obligatorio.")
    
    # --- Inserción ---
    savepoint(cn, "SP_PUBLICAR_PRODUCTO")
    
    producto_data = {
        "titulo": titulo,
        "descripcion": descripcion,
        "precio": precio,
        "nombre_categoria": nombre_categoria,
        "imagen": data.get("imagen"),
        "username_vendedor": username_vendedor,
    }
    
    new_id = productos_repo.insert_producto(cn, producto_data)
    return new_id


def consultar_producto(cn, id_producto: int) -> dict:
    """RF2.4: Consulta un producto por ID.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
    
    Returns:
        Dict con datos del producto
    
    Raises:
        ValueError: Si el producto no existe o no está disponible
    """
    producto = productos_repo.get_producto(cn, id_producto)
    
    if not producto:
        raise ValueError(f"El producto con ID {id_producto} no existe.")
    
    if not producto.get("disponible"):
        raise ValueError(f"El producto con ID {id_producto} no está disponible.")
    
    return producto


def get_categorias(cn) -> list[str]:
    """Obtiene la lista de categorías disponibles.
    
    Args:
        cn: Conexión a la base de datos
    
    Returns:
        Lista de nombres de categorías
    """
    return productos_repo.get_todas_categorias(cn)


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
