import base64
from io import BytesIO
from PIL import Image

# Logo TikiTún en base64 (naranja 1024x1024)
LOGO_BASE64 = """
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==
"""

def get_logo_image(size=(100, 100)):
    """
    Retorna la imagen del logo redimensionada.
    
    Args:
        size: Tupla (ancho, alto) para redimensionar
    
    Returns:
        PIL Image object
    """
    try:
        # Decodificar base64
        logo_bytes = base64.b64decode(LOGO_BASE64)
        img = Image.open(BytesIO(logo_bytes))
        img = img.resize(size, Image.Resampling.LANCZOS)
        return img
    except Exception as e:
        print(f"Error al cargar logo: {e}")
        return None
