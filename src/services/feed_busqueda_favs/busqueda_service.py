"""
Servicios de búsqueda de productos.
Responsable: Daniel Hidalgo

Requisitos Funcionales implementados:
- RF3.5: Hacer una búsqueda
"""

from src.repositories.feed_busqueda_favs import busqueda_repo


def obtener_categorias_disponibles(cn) -> list[str]:
    """Obtiene todas las categorías disponibles de la BD.
    
    Args:
        cn: Conexión a la base de datos
    
    Returns:
        Lista de nombres de categorías ordenados alfabéticamente
    """
    print(" [SERVICE busqueda] obtener_categorias_disponibles()")
    return busqueda_repo.get_categorias(cn)


# Órdenes válidos
ORDENES_VALIDOS = ["rating", "precio_asc", "precio_desc"]


def buscar_productos(cn, texto: str = "", categoria: str = None, orden: str = "rating") -> list[dict]:
    """RF3.5: Busca productos según filtros del usuario.
    
    Args:
        cn: Conexión a la base de datos
        texto: Cadena de búsqueda (fuzzy search en título) - opcional, vacío = sin filtro
        categoria: Categoría específica (opcional, None = todas las categorías)
        orden: Modo de ordenación:
               - "rating" (default): por puntuación del vendedor DESC
               - "precio_asc": por precio ASC, luego puntuación DESC
               - "precio_desc": por precio DESC, luego puntuación DESC
    
    Returns:
        Lista de productos ordenados
    """
    print(f" [SERVICE busqueda] buscar_productos() texto='{texto}', categoria='{categoria}', orden='{orden}'")
    
    # Normalizar texto (puede estar vacío)
    texto_limpio = texto.strip() if texto else ""
    
    # Normalizar categoría
    categoria_limpia = None
    if categoria and categoria.strip() and categoria.strip() != "(Todas)":
        categoria_limpia = categoria.strip()
    
    # Validar orden
    orden_limpio = orden if orden in ORDENES_VALIDOS else "rating"
    
    # Construir filtros
    filtros = {
        "q": texto_limpio,
        "categoria": categoria_limpia,
        "orden": orden_limpio
    }
    
    return busqueda_repo.get_busqueda(cn, filtros)
