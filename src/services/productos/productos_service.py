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
        cambios: Dict con campos a actualizar (titulo, descripcion, precio, nombre_categoria, imagen)
    
    Raises:
        ValueError: Si no es el vendedor o validaciones fallan
    """
    # Verificar que el producto existe y está disponible
    producto = productos_repo.get_producto(cn, id_producto)
    if not producto:
        raise ValueError(f"El producto con ID {id_producto} no existe.")
    
    if not producto.get("disponible"):
        raise ValueError(f"El producto con ID {id_producto} no está disponible.")
    
    # Verificar que el usuario es el vendedor
    if producto.get("username_vendedor") != username_vendedor:
        raise ValueError("No tienes permiso para modificar este producto.")
    
    # Validar cambios
    cambios_validados = {}
    
    # Título (RS2.6)
    if "titulo" in cambios:
        titulo = cambios["titulo"].strip() if cambios["titulo"] else ""
        if not titulo:
            raise ValueError("El título no puede estar vacío.")
        if len(titulo) > MAX_TITULO_LENGTH:
            raise ValueError(f"El título no puede superar {MAX_TITULO_LENGTH} caracteres.")
        cambios_validados["titulo"] = titulo
    
    # Descripción (RS2.6)
    if "descripcion" in cambios:
        descripcion = cambios["descripcion"].strip() if cambios["descripcion"] else ""
        if len(descripcion) > MAX_DESCRIPCION_LENGTH:
            raise ValueError(f"La descripción no puede superar {MAX_DESCRIPCION_LENGTH} caracteres.")
        cambios_validados["descripcion"] = descripcion
    
    # Precio (RS2.2)
    if "precio" in cambios:
        try:
            precio = float(cambios["precio"])
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que 0.")
        cambios_validados["precio"] = round(precio, 2)
    
    # Categoría (RS2.4)
    if "nombre_categoria" in cambios:
        categoria = cambios["nombre_categoria"].strip() if cambios["nombre_categoria"] else ""
        if not categoria:
            raise ValueError("Debe seleccionar una categoría.")
        if not productos_repo.categoria_existe(cn, categoria):
            raise ValueError(f"La categoría '{categoria}' no es válida.")
        cambios_validados["nombre_categoria"] = categoria
    
    # Imagen
    if "imagen" in cambios:
        cambios_validados["imagen"] = cambios["imagen"]
    
    if not cambios_validados:
        return  # No hay cambios
    
    savepoint(cn, "SP_MODIFICAR_PRODUCTO")
    productos_repo.update_producto(cn, id_producto, cambios_validados)


def eliminar_producto(cn, id_producto: int, username_vendedor: str) -> None:
    """RF2.3: Elimina un producto (marca como no disponible).
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
        username_vendedor: Vendedor (para verificar permisos)
    
    Raises:
        ValueError: Si no es el vendedor, producto no existe, o producto en proceso de venta
    """
    # Verificar que el producto existe
    producto = productos_repo.get_producto(cn, id_producto)
    if not producto:
        raise ValueError(f"El producto con ID {id_producto} no existe.")
    
    if not producto.get("disponible"):
        raise ValueError(f"El producto con ID {id_producto} ya no está disponible.")
    
    # Verificar que el usuario es el vendedor
    if producto.get("username_vendedor") != username_vendedor:
        raise ValueError("No tienes permiso para eliminar este producto.")
    
    # TODO: Verificar que no está en proceso de venta (contraoferta activa o venta pendiente)
    # Esto requeriría consultar la tabla Vendido y Contraoferta
    # Por ahora lo dejamos pendiente de implementar en RF4
    
    savepoint(cn, "SP_ELIMINAR_PRODUCTO")
    productos_repo.soft_delete_producto(cn, id_producto)


def promocionar_producto(cn, id_producto: int, username_vendedor: str, 
                        grado_promocion: float) -> float:
    """RF2.5: Promociona un producto incrementando su visibilidad.
    
    Coste: grado_promocion * 0.1 * precio_producto
    
    RS aplicadas:
    - RS2.7: Solo el propietario puede promocionar
    - RS2.10: Grado de promoción en [0, 1] con 2 decimales
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
        username_vendedor: Vendedor (para cobrar del saldo)
        grado_promocion: Valor entre 0 y 1
    
    Returns:
        Coste de la promoción
    
    Raises:
        ValueError: Si saldo insuficiente o valor no válido
    """
    from src.repositories.perfiles import usuarios_repo
    
    # Validar grado_promocion (RS2.10)
    try:
        grado_promocion = float(grado_promocion)
    except (TypeError, ValueError):
        raise ValueError("El grado de promoción debe ser un número válido.")
    
    if grado_promocion < 0 or grado_promocion > 1:
        raise ValueError("El grado de promoción debe estar entre 0 y 1.")
    
    # Redondear a 2 decimales
    grado_promocion = round(grado_promocion, 2)
    
    # Obtener producto
    producto = productos_repo.get_producto(cn, id_producto)
    if not producto:
        raise ValueError(f"El producto con ID {id_producto} no existe.")
    
    if not producto.get("disponible"):
        raise ValueError(f"El producto con ID {id_producto} no está disponible.")
    
    # Verificar que el usuario es el vendedor (RS2.7)
    if producto.get("username_vendedor") != username_vendedor:
        raise ValueError("No tienes permiso para promocionar este producto.")
    
    # Calcular coste
    precio = producto.get("precio", 0)
    coste = round(grado_promocion * 0.1 * precio, 2)
    
    if coste <= 0:
        # Si grado = 0, no hay coste pero actualizamos igualmente
        savepoint(cn, "SP_PROMOCIONAR_PRODUCTO")
        productos_repo.update_promocion(cn, id_producto, grado_promocion)
        return 0.0
    
    # Obtener saldo del usuario
    usuario = usuarios_repo.get_usuario(cn, username_vendedor)
    if not usuario:
        raise ValueError("No se pudo obtener la información del usuario.")
    
    saldo_actual = usuario.get("saldo", 0)
    
    # Verificar saldo suficiente
    if saldo_actual < coste:
        raise ValueError(
            f"Saldo insuficiente. El coste es {coste:.2f}€ "
            f"y tu saldo es {saldo_actual:.2f}€."
        )
    
    # Realizar transacción
    savepoint(cn, "SP_PROMOCIONAR_PRODUCTO")
    
    # Descontar del monedero
    nuevo_saldo = round(saldo_actual - coste, 2)
    usuarios_repo.update_saldo(cn, username_vendedor, nuevo_saldo)
    
    # Actualizar promoción del producto
    productos_repo.update_promocion(cn, id_producto, grado_promocion)
    
    return coste
