"""
Repositorio de consultas de búsqueda de productos.
Responsable: Daniel Hidalgo

Consultas con filtrado fuzzy y ordenación.
"""


def search_productos(cn, username: str, filtros: dict) -> list[dict]:
    """Busca productos según filtros.
    
    Filtros:
    - q: búsqueda fuzzy en título (LIKE %query%)
    - categoria: filtro por categoría
    - orden_precio: "asc" o "desc"
    
    Siempre filtra por:
    - disponible = true
    - rango de distancia del usuario
    
    Orden por defecto: puntuación vendedor DESC
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario que busca
        filtros: Dict con parámetros de búsqueda
    
    Returns:
        Lista de productos ordenados
    """
    print("   [REPO busqueda] search_productos()", username, filtros)
    # TODO: Implementar consulta con filtros dinámicos
    # TODO: Usar UPPER(titulo) LIKE UPPER(?) para fuzzy search
    return []  # Demo
