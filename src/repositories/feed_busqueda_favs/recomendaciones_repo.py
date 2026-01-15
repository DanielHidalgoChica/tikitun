"""
Repositorio de consultas para el feed de recomendaciones.
Responsable: Daniel Hidalgo

Consultas complejas para obtener productos recomendados.
"""


def get_recomendaciones(cn, username: str) -> list[dict]:
    """Obtiene productos recomendados para el usuario.
    
    Lógica compleja:
    1. JOIN USUARIO para obtener categorías preferidas, ubicación, rango
    2. JOIN PRODUCTO filtrando por categorías y disponibilidad
    3. JOIN USUARIO (vendedor) para obtener ubicación y puntuación
    4. Calcular distancia entre ubicaciones
    5. Filtrar por rango (distancia <= rango_usuario + rango_vendedor)
    6. Ordenar por: categoría IN preferidas DESC, promocion DESC, valoracion_vendedor DESC, RANDOM()
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
    
    Returns:
        Lista ordenada de productos
    

    Por ahora lo único que hace es pillar todos los productos disponibles de la base de datos
    Returns:
        Lista de todos los productos con disponible = 1
    """
    print("   [REPO recomendaciones] get_recomendaciones()", username)
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
    
    cur.close()
    return productos   
    # TODO: Implementar consulta compleja
    # TODO: Usar función de distancia geográfica (ej: Haversine)