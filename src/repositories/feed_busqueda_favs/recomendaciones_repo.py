"""
Repositorio de consultas para el feed de recomendaciones.
Responsable: Daniel Hidalgo

Consultas complejas para obtener productos recomendados.
Implementa RF3.1 y RF3.5 con filtrado por ubicación y categorías preferidas.
"""

import math


def calcular_distancia_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula distancia en km entre dos coordenadas usando fórmula Haversine.
    
    Args:
        lat1, lon1: Coordenadas punto 1 (latitud, longitud en grados decimales)
        lat2, lon2: Coordenadas punto 2
    
    Returns:
        Distancia en kilómetros (float)
    """
    # Radio de la Tierra en km
    R = 6371.0
    
    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Diferencias
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Fórmula Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def get_recomendaciones(cn, username: str) -> list[dict]:
    """RF3.1 y RF3.5: Obtiene productos recomendados personalizados para el usuario.
    
    Algoritmo:
    1. Obtener ubicación (ubi_latitud, ubi_longitud) y rango del usuario
    2. Obtener categorías preferidas del usuario (tabla Preferidos)
    3. Query: Productos disponibles con info de vendedor (ubicación, rating)
    4. Filtrar por distancia: dist(usuario, vendedor) <= rango_usuario + rango_vendedor
    5. Ordenar por:
       - Categoría en preferidas (DESC - primero las preferidas)
       - Promoción (DESC - mayor descuento primero)
       - Valoración del vendedor (DESC - mejor rating primero)
       - Aleatorio (para desempates)
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario que consulta el feed
    
    Returns:
        Lista de dicts con productos recomendados, incluyendo campos de debug:
        - id_producto, titulo, descripcion, precio
        - username_vendedor, nombre_categoria, promocion, disponible
        - valoracion_vendedor (float)
        - en_preferidas (bool) - si categoría está en preferidas del usuario
        - distancia_km (float) - distancia calculada usuario-vendedor
    """
    print("   [REPO recomendaciones] get_recomendaciones()", username)
    cur = cn.cursor()
    
    # PASO 1: Obtener ubicación y rango del usuario
    cur.execute("""
        SELECT ubi_latitud, ubi_longitud, rango
        FROM usuario
        WHERE username = ?
    """, (username,))
    
    row = cur.fetchone()
    if not row:
        cur.close()
        return []
    
    user_lat, user_lon, user_rango = row[0], row[1], row[2]
    print(f"   [DEBUG] Usuario {username}: lat={user_lat}, lon={user_lon}, rango={user_rango} km")
    
    # PASO 2: Obtener categorías preferidas del usuario
    cur.execute("""
        SELECT nombre
        FROM preferidos
        WHERE username = ?
    """, (username,))
    
    preferidas = set(row[0] for row in cur.fetchall())
    print(f"   [DEBUG] Categorías preferidas de {username}: {preferidas}")
    
    # PASO 3: Query de productos + info vendedor
    cur.execute("""
        SELECT 
            p.id_producto,
            p.titulo,
            p.descripcion,
            p.precio,
            p.username AS username_vendedor,
            p.nombre_categoria,
            p.promocion,
            p.disponible,
            u_vendedor.ubi_latitud,
            u_vendedor.ubi_longitud,
            u_vendedor.rango,
            u_vendedor.valoracion_media
        FROM producto p
        JOIN usuario u_vendedor ON p.username = u_vendedor.username
        WHERE p.disponible = 1
    """)
    
    productos = []
    for row in cur.fetchall():
        id_prod = row[0]
        titulo = row[1]
        desc = row[2]
        precio = row[3]
        vendedor = row[4]
        categoria = row[5]
        promocion = row[6] or 0  # NULL → 0
        disponible = row[7]
        vendedor_lat = row[8]
        vendedor_lon = row[9]
        vendedor_rango = row[10] or 0  # NULL → 0
        valoracion_vendedor = row[11] or 0  # NULL → 0
        
        # PASO 4a: Filtrar por rango: distancia <= rango_usuario + rango_vendedor
        distancia = calcular_distancia_haversine(
            user_lat, user_lon, 
            vendedor_lat, vendedor_lon
        )
        
        rango_total = user_rango + vendedor_rango
        if distancia > rango_total:
            print(f"   [DEBUG DESCARTADO] Producto {id_prod} ({titulo}): FUERA DE RANGO - distancia={distancia:.2f}km > rango_total={rango_total}km (usuario={user_rango}km + vendedor={vendedor_rango}km)")
            continue  # Vendedor fuera de rango, descartar
        
        # PASO 4b: Filtrar por categoría preferida
        en_preferidas = categoria in preferidas
        if not en_preferidas:
            print(f"   [DEBUG DESCARTADO] Producto {id_prod} ({titulo}): CATEGORÍA NO PREFERIDA - categoria='{categoria}' no está en {preferidas}")
            continue  # Categoría no preferida, descartar
        
        # Agregar a resultados (incluir datos de debug)
        print(f"   [DEBUG INCLUIDO] Producto {id_prod} ({titulo}): promocion={promocion}, vendedor_rating={valoracion_vendedor}, distancia={distancia:.2f}km")
        productos.append({
            "id_producto": id_prod,
            "titulo": titulo,
            "descripcion": desc,
            "precio": precio,
            "username_vendedor": vendedor,
            "nombre_categoria": categoria,
            "promocion": promocion,
            "disponible": disponible,
            "valoracion_vendedor": valoracion_vendedor,
            "en_preferidas": en_preferidas,
            "distancia_km": round(distancia, 2)
        })
    
    cur.close()
    
    # PASO 5: Ordenamiento simple: Promoción DESC → Valoración vendedor DESC
    productos.sort(
        key=lambda prod: (
            -(prod["promocion"] or 0),  # Negado para DESC
            -(prod["valoracion_vendedor"] or 0)  # Negado para DESC
        )
    )
    
    print(f"   [DEBUG RESULTADO FINAL] Se retornan {len(productos)} productos de los consultados")
    
    return productos