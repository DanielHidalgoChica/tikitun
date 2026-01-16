"""
Repositorio de acceso a datos de productos.
Responsable: Roberto González

Operaciones CRUD sobre la tabla PRODUCTO.
"""


def _get_next_id_producto(cn) -> int:
    """Obtiene el siguiente ID disponible para un producto.
    
    Oracle no tiene AUTOINCREMENT, así que usamos MAX(id_producto) + 1.
    """
    cur = cn.cursor()
    cur.execute("SELECT COALESCE(MAX(id_producto), 0) + 1 FROM Producto")
    row = cur.fetchone()
    cur.close()
    return row[0] if row else 1


def insert_producto(cn, producto: dict) -> int:
    """Inserta un nuevo producto en la BD.
    
    Args:
        cn: Conexión a la base de datos
        producto: Dict con:
            - titulo: str (max 80 chars)
            - descripcion: str (max 500 chars, opcional)
            - precio: float (>0)
            - nombre_categoria: str (debe existir en Categoria)
            - imagen: bytes (opcional, BLOB)
            - username_vendedor: str (FK a Usuario)
    
    Returns:
        id_producto generado
    """
    new_id = _get_next_id_producto(cn)
    
    cur = cn.cursor()
    cur.execute("""
        INSERT INTO Producto (
            id_producto,
            username,
            nombre_categoria,
            titulo,
            descripcion,
            precio,
            imagen,
            promocion,
            disponible
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_id,
        producto.get("username_vendedor"),
        producto.get("nombre_categoria"),
        producto.get("titulo"),
        producto.get("descripcion", ""),
        float(producto.get("precio", 0)),
        producto.get("imagen"),  # BLOB o None
        0,  # promocion default 0
        1   # disponible = true
    ))
    cur.close()
    
    return new_id


def categoria_existe(cn, nombre_categoria: str) -> bool:
    """Verifica si una categoría existe en la BD.
    
    Args:
        cn: Conexión a la base de datos
        nombre_categoria: Nombre de la categoría a verificar
    
    Returns:
        True si existe, False en caso contrario
    """
    cur = cn.cursor()
    cur.execute("SELECT COUNT(*) FROM Categoria WHERE nombre = ?", (nombre_categoria,))
    row = cur.fetchone()
    cur.close()
    return row[0] > 0 if row else False


def get_todas_categorias(cn) -> list[str]:
    """Obtiene todas las categorías disponibles.
    
    Args:
        cn: Conexión a la base de datos
    
    Returns:
        Lista de nombres de categorías
    """
    cur = cn.cursor()
    cur.execute("SELECT nombre FROM Categoria ORDER BY nombre")
    categorias = [row[0] for row in cur.fetchall()]
    cur.close()
    return categorias


def get_producto(cn, id_producto: int) -> dict | None:
    """Obtiene un producto por ID.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
    
    Returns:
        Dict con datos del producto o None si no existe
    """
    cur = cn.cursor()
    cur.execute("""
        SELECT 
            p.id_producto,
            p.username,
            p.nombre_categoria,
            p.titulo,
            p.descripcion,
            p.precio,
            p.promocion,
            p.disponible,
            p.imagen,
            u.valoracion_media,
            u.ubi_latitud,
            u.ubi_longitud
        FROM Producto p
        LEFT JOIN Usuario u ON p.username = u.username
        WHERE p.id_producto = ?
    """, (id_producto,))
    
    row = cur.fetchone()
    cur.close()
    
    if not row:
        return None
    
    return {
        "id_producto": row[0],
        "username_vendedor": row[1],
        "nombre_categoria": row[2],
        "titulo": row[3],
        "descripcion": row[4],
        "precio": row[5],
        "promocion": row[6],
        "disponible": row[7],
        "imagen": row[8],
        "valoracion_vendedor": row[9],
        "latitud_vendedor": row[10],
        "longitud_vendedor": row[11],
    }


def update_producto(cn, id_producto: int, cambios: dict) -> None:
    """Actualiza campos de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
        cambios: Dict con campos a modificar. Campos permitidos:
            - titulo
            - descripcion
            - precio
            - nombre_categoria
            - imagen
    """
    # Mapeo de campos del dict a columnas de la tabla
    campos_permitidos = {
        "titulo": "titulo",
        "descripcion": "descripcion",
        "precio": "precio",
        "nombre_categoria": "nombre_categoria",
        "imagen": "imagen",
    }
    
    # Construir SET dinámicamente solo con campos presentes
    set_clauses = []
    valores = []
    
    for campo, columna in campos_permitidos.items():
        if campo in cambios:
            set_clauses.append(f"{columna} = ?")
            valores.append(cambios[campo])
    
    if not set_clauses:
        return  # No hay nada que actualizar
    
    valores.append(id_producto)
    
    cur = cn.cursor()
    cur.execute(f"""
        UPDATE Producto
        SET {', '.join(set_clauses)}
        WHERE id_producto = ?
    """, tuple(valores))
    cur.close()


def soft_delete_producto(cn, id_producto: int) -> None:
    """Marca un producto como no disponible (soft delete).
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
    """
    cur = cn.cursor()
    cur.execute("UPDATE Producto SET disponible = 0 WHERE id_producto = ?", (id_producto,))
    cur.close()


def get_all_productos(cn) -> list[dict]:
    """Obtiene todos los productos disponibles.
    
    Args:
        cn: Conexión a la base de datos
    
    Returns:
        Lista de todos los productos con disponible = 1
    """
    cur = cn.cursor()
    cur.execute("""
        SELECT 
            p.id_producto,
            p.titulo,
            p.descripcion,
            p.precio,
            p.username AS username_vendedor,
            p.nombre_categoria,
            p.promocion,
            p.disponible
        FROM producto p
        WHERE p.disponible = 1
        ORDER BY p.id_producto DESC
    """)
    
    productos = []
    for row in cur.fetchall():
        productos.append({
            "id_producto": row[0],
            "titulo": row[1],
            "descripcion": row[2],
            "precio": row[3],
            "username_vendedor": row[4],
            "nombre_categoria": row[5],
            "promocion": row[6],
            "disponible": row[7]
        })
    
    return productos


def search_productos(cn, filtros: dict) -> list[dict]:
    """Busca productos según filtros.
    
    Args:
        cn: Conexión a la base de datos
        filtros: Dict con q (query), categoria, orden, etc.
    
    Returns:
        Lista de productos que coinciden
    """
    print("   [REPO productos] search_productos()", filtros)
    # TODO: SELECT * FROM PRODUCTO WHERE disponible = true AND ...
    
    # Demo (eliminar cuando implementes)
    return [
        {"id_producto": 1, "titulo": "Producto 1", "precio": 29.99},
        {"id_producto": 2, "titulo": "Producto 2", "precio": 49.99},
    ]


def update_promocion(cn, id_producto: int, grado_promocion: float) -> None:
    """Actualiza el grado de promoción de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: ID del producto
        grado_promocion: Valor entre 0 y 1 con 2 decimales
    """
    cur = cn.cursor()
    cur.execute("""
        UPDATE Producto 
        SET promocion = ?
        WHERE id_producto = ?
    """, (grado_promocion, id_producto))
    cur.close()
