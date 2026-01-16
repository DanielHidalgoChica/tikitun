"""
Servicios de búsqueda de productos.
Responsable: Daniel Hidalgo

Requisitos Funcionales implementados:
- RF3.5: Hacer una búsqueda
"""

from src.repositories.feed_busqueda_favs import busqueda_repo


# Categorías disponibles para búsqueda
CATEGORIAS_DISPONIBLES = [
    "Vehículos",
    "Moda",
    "Tecnología",
    "Deportes",
    "Hogar",
    "Libros"
]

# Órdenes válidos
ORDENES_VALIDOS = ["rating", "precio_asc", "precio_desc"]


def buscar_productos(cn, texto: str, categoria: str = None, orden: str = "rating") -> list[dict]:
    """RF3.5: Busca productos según filtros del usuario.
    
    Args:
        cn: Conexión a la base de datos
        texto: Cadena de búsqueda (fuzzy search en título) - OBLIGATORIO
        categoria: Categoría específica (opcional, None = todas las categorías)
        orden: Modo de ordenación:
               - "rating" (default): por puntuación del vendedor DESC
               - "precio_asc": por precio ASC, luego puntuación DESC
               - "precio_desc": por precio DESC, luego puntuación DESC
    
    Returns:
        Lista de productos ordenados
    
    Raises:
        ValueError: Si el texto de búsqueda está vacío
    """
    print(f" [SERVICE busqueda] buscar_productos() texto='{texto}', categoria='{categoria}', orden='{orden}'")
    
    # Validar texto obligatorio
    texto_limpio = texto.strip() if texto else ""
    if not texto_limpio:
        raise ValueError("El texto de búsqueda es obligatorio")
    
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
