"""
Servicios de búsqueda de productos.
Responsable: Daniel Hidalgo

Requisitos Funcionales implementados:
- RF3.5: Hacer una búsqueda
"""

from src.repositories.feed_busqueda_favs import busqueda_repo


def buscar_productos(cn, username: str, filtros: dict) -> list[dict]:
    """RF3.5: Busca productos según filtros del usuario.
    
    Filtros:
    - q: Cadena de búsqueda (fuzzy search en título)
    - categoria: Categoría específica (opcional)
    - orden_precio: "asc" o "desc" (opcional, por defecto orden por puntuación)
    
    Siempre filtra por rango de distancia.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario que busca
        filtros: Dict con q, categoria, orden_precio
    
    Returns:
        Lista de productos ordenados
    """
    print(" [SERVICE busqueda] buscar_productos()")
    return busqueda_repo.search_productos(cn, username, filtros)
