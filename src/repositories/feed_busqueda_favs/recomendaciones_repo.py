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
    """
    print("   [REPO recomendaciones] get_recomendaciones()", username)
    # TODO: Implementar consulta compleja
    # TODO: Usar función de distancia geográfica (ej: Haversine)
    return []  # Demo
