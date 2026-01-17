"""
Servicios de feed de recomendaciones.
Responsable: Daniel Hidalgo

Requisitos Funcionales implementados:
- RF3.1: Mostrar las recomendaciones
"""

from src.repositories.feed_busqueda_favs import recomendaciones_repo


def obtener_feed(cn, username: str) -> list[dict]:
    """RF3.1: Obtiene productos recomendados para el usuario.
    
    Criterios:
    1. Filtrar por categorías preferidas del usuario
    2. Filtrar por rango de distancia (ubicación + rango km)
    3. Ordenar por:
       - Categoría preferida → grado de promoción DESC → puntuación vendedor DESC → aleatorio
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario que consulta el feed
    
    Returns:
        Lista ordenada de productos recomendados
    """
    return recomendaciones_repo.get_recomendaciones(cn, username)
