"""
Repositorio de consultas de búsqueda de productos.
Responsable: Daniel Hidalgo

Consultas con filtrado fuzzy y ordenación.
RF3.5: Búsqueda de productos por texto y categoría.
"""


def get_busqueda(cn, filtros: dict) -> list[dict]:
    """Busca productos según filtros.
    
    Filtros esperados:
    - q: búsqueda fuzzy en título (obligatorio, LIKE %query%)
    - categoria: filtro por categoría (opcional, None = todas)
    - orden: "rating" (default), "precio_asc", "precio_desc"
    
    Siempre filtra por disponible = 1.
    
    Ordenación:
    - "rating": valoracion_media DESC
    - "precio_asc": precio ASC, valoracion_media DESC
    - "precio_desc": precio DESC, valoracion_media DESC
    
    Args:
        cn: Conexión a la base de datos
        filtros: Dict con parámetros de búsqueda
    
    Returns:
        Lista de productos ordenados
    """
    q = filtros.get("q", "").strip()
    categoria = filtros.get("categoria")
    orden = filtros.get("orden", "rating")
    
    print(f"   [REPO busqueda] get_busqueda() q='{q}', categoria='{categoria}', orden='{orden}'")
    
    cur = cn.cursor()
    
    # Construir query dinámica
    query = """
        SELECT 
            p.id_producto,
            p.titulo,
            p.descripcion,
            p.precio,
            p.username AS username_vendedor,
            p.nombre_categoria,
            p.promocion,
            p.disponible,
            p.num_favs,
            p.imagen,
            u.valoracion_media
        FROM producto p
        JOIN usuario u ON p.username = u.username
        WHERE p.disponible = 1
    """
    
    params = []
    
    # Filtro por texto de búsqueda (opcional)
    if q:
        query += " AND LOWER(p.titulo) LIKE '%' || LOWER(?) || '%'"
        params.append(q)
    
    # Filtro por categoría (opcional)
    if categoria and categoria.strip():
        query += " AND p.nombre_categoria = ?"
        params.append(categoria.strip())
    
    # Ordenación
    if orden == "precio_asc":
        query += " ORDER BY p.precio ASC, u.valoracion_media DESC"
    elif orden == "precio_desc":
        query += " ORDER BY p.precio DESC, u.valoracion_media DESC"
    else:  # default: rating
        query += " ORDER BY u.valoracion_media DESC"
    
    print(f"   [DEBUG BUSQUEDA] Query: {query}")
    print(f"   [DEBUG BUSQUEDA] Params: {params}")
    
    cur.execute(query, params)
    
    productos = []
    for row in cur.fetchall():
        productos.append({
            "id_producto": row[0],
            "titulo": row[1],
            "descripcion": row[2],
            "precio": row[3],
            "username_vendedor": row[4],
            "nombre_categoria": row[5],
            "promocion": row[6] or 0,
            "disponible": row[7],
            "num_favs": row[8] or 0,
            "imagen": row[9],
            "valoracion_vendedor": row[10] or 0
        })
    
    cur.close()
    
    print(f"   [DEBUG BUSQUEDA] Encontrados {len(productos)} productos")
    
    return productos


def get_categorias(cn) -> list[str]:
    """Obtiene todas las categorías disponibles de la tabla Categoria.
    
    Args:
        cn: Conexión a la base de datos
    
    Returns:
        Lista de nombres de categorías ordenados alfabéticamente
    """
    print("   [REPO busqueda] get_categorias()")
    
    cur = cn.cursor()
    cur.execute("SELECT nombre FROM categoria ORDER BY nombre ASC")
    
    categorias = [row[0] for row in cur.fetchall()]
    cur.close()
    
    print(f"   [DEBUG BUSQUEDA] Categorías obtenidas de la BD: {categorias}")
    
    return categorias
