"""
Servicios de gestión de perfiles de usuario.
Responsable: Eisa Rodríguez

Requisitos Funcionales implementados:
- RF1.1: Dar de alta al usuario
- RF1.2: Consultar perfil de usuario
- RF1.3: Modificar perfil de usuario
- RF1.4: Añadir saldo al monedero
- RF1.5: Transferir saldo a cuenta bancaria
- RF1.6: Dar de baja al usuario
"""

from src.db.db_app import savepoint
from src.repositories.perfiles import usuarios_repo
from src.services.productos.productos_service import get_productos_usuario, eliminar_producto
from src.services.ventas.ventas_service import obtener_ventas_usuario, consultar_contraofertas, obtener_ventas_como_comprador
import re


_PW_REQUIRES = [r"[A-Z]", r"[a-z]", r"[0-9]", r"[^A-Za-z0-9]"]


def verificar_credenciales(cn, username: str, contraseña: str) -> bool:
    """Verifica si las credenciales de un usuario son correctas.
    
    Args:
        cn: Conexión a la base de datos
        username: Nombre de usuario
        contraseña: Contraseña a verificar
    
    Returns:
        True si las credenciales son válidas, False en caso contrario
    
    Raises:
        ValueError: Si el usuario no existe
    """
    usuario = usuarios_repo.get_usuario(cn, username)
    if usuario is None:
        raise ValueError(f"Usuario {username} no existe")
    
    # Delegar la verificación al repositorio
    return usuarios_repo.verificar_contraseña(cn, username, contraseña)


def dar_alta_usuario(cn, data: dict) -> None:
    """RF1.1: Registra un nuevo usuario en el sistema.
    
    RS aplicadas:
    - RS1.1: Usuario debe ser mayor de edad
    - RS1.2: Nombre de usuario y correo únicos
    - RS1.4: Contraseña con requisitos de complejidad
    - RS1.5: Aceptar política de privacidad
    - RS1.6: Entre 1 y 6 categorías de preferencia
    - RS1.17: Rango de interés positivo
    
    Args:
        cn: Conexión a la base de datos
        data: Dict con nombre_completo, username, contraseña, correo,
              ubicacion, rango, categorias_preferidas, mayor_edad, acepta_politica
    
    Raises:
        ValueError: Si no cumple validaciones
    """
    # Validaciones según RDE/RD
    nombre = data.get("nombre_completo")
    username = data.get("username")
    contraseña = data.get("contraseña") or data.get("contrasenia")
    correo = data.get("correo")
    ubicacion = data.get("ubicacion")
    rango = data.get("rango")
    categorias = data.get("categorias") or data.get("categorias_preferidas") or data.get("categorias_preferencia")
    mayoria = data.get("mayoria_edad")
    acepta = data.get("aceptacion_politicas")

    # Campos obligatorios
    if not all([nombre, username, contraseña, correo, ubicacion, rango, categorias]):
        raise ValueError("Faltan campos obligatorios para el alta")
    # Edad y aceptación
    if not mayoria:
        raise ValueError("El usuario debe confirmar que es mayor de edad")
    if not acepta:
        raise ValueError("El usuario debe aceptar la política de privacidad y condiciones")
    # username
    if len(username) > 15:
        raise ValueError("Nombre de usuario demasiado largo (máx. 15)")
    # contraseña: longitud y contenido
    if not (8 <= len(contraseña) <= 15):
        raise ValueError("La contraseña debe tener entre 8 y 15 caracteres")
    if " " in contraseña:
        raise ValueError("La contraseña no puede contener espacios")
    for r in _PW_REQUIRES:
        if not re.search(r, contraseña):
            raise ValueError("La contraseña debe incluir mayúscula, minúscula, dígito y carácter especial")
    # correo (simple)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        raise ValueError("Correo con formato inválido")
    # ubicacion
    if not (isinstance(ubicacion, (list, tuple)) and len(ubicacion) >= 2):
        raise ValueError("Ubicación inválida (lat, lon)")
    try:
        lat = float(ubicacion[0]); lon = float(ubicacion[1])
    except Exception:
        raise ValueError("Latitud/longitud no numéricas")
    # rango
    try:
        rango_f = float(rango)
        if rango_f < 0:
            raise ValueError()
    except Exception:
        raise ValueError("Rango debe ser número real positivo (2 decimales)")
    # categorias
    if not isinstance(categorias, (list, tuple)):
        raise ValueError("Categorías debe ser lista")
    if not (1 <= len(categorias) <= 6):
        raise ValueError("Debe indicar entre 1 y 6 categorías de preferencia")

    # Unicidad username (repositorio debe proporcionar comprobación definitiva)
    existing = usuarios_repo.get_usuario(cn, username)
    if existing is not None:
        raise ValueError("Nombre de usuario ya existe")

    # Preparar dict definitivo para repositorio
    usuario = {
        "username": username,
        "contraseña": contraseña,
        "nombre_completo": nombre,
        "correo": correo,
        "ubicacion": (lat, lon),
        "rango": round(rango_f, 2),
        "categorias": list(categorias),
        "mayoria_edad": bool(mayoria),
        "aceptacion_politicas": bool(acepta),
        "saldo": float(data.get("saldo", 0.0)),
        "valoracion_media": data.get("valoracion_media"),
        "cuenta_eliminada": False,
    }

    # Persistir usando el repositorio (cn debe ser proporcionado por el llamador)
    usuarios_repo.insert_usuario(cn, usuario)


def consultar_perfil(cn, username: str) -> dict:
    """RF1.2: Obtiene información de un perfil de usuario.
    
    RS aplicadas:
    - RS1.12: Usuario debe existir y no estar eliminado
    
    Args:
        cn: Conexión a la base de datos
        username: Nombre de usuario a consultar
    
    Returns:
        Dict con información del perfil
    
    Raises:
        ValueError: Si usuario no existe o cuenta eliminada
    """
    print(" [SERVICE perfiles] consultar_perfil()")
    usuario = usuarios_repo.get_usuario(cn, username)
    if usuario is None or usuario.get("cuenta_eliminada"):
        raise ValueError("Usuario no existe o cuenta eliminada")
    
    # Devolver sólo campos permitidos
    return {k: usuario[k] for k in (
        "username", "nombre_completo", "correo", "ubicacion", "rango", "categorias", "mayoria_edad", "aceptacion_politicas", "saldo", "valoracion_media"
    )}


def modificar_perfil(cn, username: str, cambios: dict) -> None:
    """RF1.3: Modifica los datos de un perfil de usuario existente.
    
    RS aplicadas:
    - RS1.3: Usuario debe existir y no estar eliminado
    - RS1.7: Campos a modificar válidos y en formato correcto
    
    Args:
        cn: Conexión a la base de datos
        username: Nombre de usuario a modificar
        cambios: Diccionario con los cambios a aplicar (campos válidos: nombre_completo, correo, ubicacion, rango, categorias, mayor_edad, acepta_politica)
    
    Raises:
        ValueError: Si usuario no existe, cuenta eliminada o cambios inválidos
    """
    try:

        # Validar existencia del usuario
        usuario = usuarios_repo.get_usuario(cn, username)
        if not usuario or usuario.get("cuenta_eliminada"):
            raise ValueError("El usuario no existe o ha sido eliminado")

        correo = cambios.get("correo")
        if correo:
            if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", correo):
                raise ValueError("Formato de correo inválido")

        lat = cambios.get("ubi_latitud")
        lon = cambios.get("ubi_longitud")
        if lat or lon:
            if not lat or not lon:
                raise ValueError("Debes proporcionar ambas coordenadas (latitud y longitud) o ninguna")
            try:
                lat = float(lat)
                lon = float(lon)
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    raise ValueError("Coordenadas fuera de rango")
            except ValueError:
                raise ValueError("Latitud y longitud deben ser números")

        rango = cambios.get("rango")
        if rango:
            try:
                rango = float(rango)
                if rango <= 0:
                    raise ValueError("El rango debe ser mayor a 0")
            except ValueError:
                raise ValueError("El rango debe ser un número")

        categorias = cambios.get("categorias", [])
        if not (1 <= len(categorias) <= 6):
            raise ValueError("Debe seleccionar entre 1 y 6 categorías preferidas")

        usuarios_repo.update_usuario(cn, username, cambios)
        usuarios_repo.update_categorias_preferidas(cn, username, categorias)
    except Exception as e:
        raise


def añadir_saldo(cn, username: str, cantidad: float) -> None:
    """RF1.4: Añade saldo al monedero del usuario.
    
    RS aplicadas:
    - RS1.8: Cantidad debe ser positiva
    - RS1.14: Usuario debe existir y no estar eliminado
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario que recarga saldo
        cantidad: Cantidad a añadir (positiva, 2 decimales)
    
    Raises:
        ValueError: Si cantidad no es positiva o usuario no existe
    """
    print(" [SERVICE perfiles] añadir_saldo()")
    usuario = usuarios_repo.get_usuario(cn, username)
    if usuario is None or usuario.get("cuenta_eliminada"):
        raise ValueError("Usuario no existe o cuenta eliminada")
    
    if cantidad <= 0:
        raise ValueError("La cantidad a añadir debe ser positiva")
    
    # Calcular nuevo saldo
    nuevo_saldo = round(usuario["saldo"] + cantidad, 2)
    
    # Actualizar saldo (repositorio maneja la persistencia)
    usuarios_repo.update_saldo(cn, username, nuevo_saldo)


def transferir_saldo(cn, username: str, cantidad: float, contraseña: str) -> None:
    """RF1.5: Transfiere saldo del monedero a cuenta bancaria.
    
    RS aplicadas:
    - RS1.9: Cantidad entre 0 y saldo disponible
    - RS1.10: Contraseña correcta
    - RS1.15: Usuario debe existir y no estar eliminado
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario que retira saldo
        cantidad: Cantidad a transferir
        contraseña: Contraseña para confirmar
    
    Raises:
        ValueError: Si saldo insuficiente o contraseña incorrecta
    """
    print(" [SERVICE perfiles] transferir_saldo()")
    usuario = usuarios_repo.get_usuario(cn, username)
    if usuario is None or usuario.get("cuenta_eliminada"):
        raise ValueError("Usuario no existe o cuenta eliminada")
    
    if cantidad <= 0 or cantidad > usuario["saldo"]:
        raise ValueError("Cantidad a transferir inválida")
    
    # Verificar contraseña
    if not usuarios_repo.verificar_contraseña(cn, username, contraseña):
        raise ValueError("La contraseña introducida es incorrecta.")
    
    # Calcular nuevo saldo
    nuevo_saldo = round(usuario["saldo"] - cantidad, 2)
    
    # Actualizar saldo (repositorio maneja la persistencia)
    usuarios_repo.update_saldo(cn, username, nuevo_saldo)


def dar_baja_usuario(cn, username: str, contraseña: str) -> None:
    """RF1.6: Elimina cuenta de usuario (soft delete).
    
    RS aplicadas:
    - RS1.11: No puede tener ventas activas
    - RS1.16: Usuario debe existir y no estar eliminado
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario a dar de baja
        contraseña: Contraseña para confirmar
    
    Raises:
        ValueError: Si tiene ventas activas o contraseña incorrecta
    """
    # Verificar existencia y contraseña
    usuario = usuarios_repo.get_usuario(cn, username)
    if not usuario or usuario.get("cuenta_eliminada"):
        raise ValueError("El usuario no existe o ya ha sido eliminado.")
    
    if not usuarios_repo.verificar_contraseña(cn, username, contraseña):
        raise ValueError("La contraseña introducida es incorrecta.")

    # Validar que no hay ventas activas (Vendedor)
    ventas_activas = obtener_ventas_usuario(cn, username)
    if len(ventas_activas) > 0:
        raise ValueError("No puedes darte de baja: tienes ventas en curso.")
    
    # Validar que no hay ventas activas (Comprador)
    ventas_como_comprador = obtener_ventas_como_comprador(cn, username)
    if len(ventas_como_comprador) > 0:
        raise ValueError("No puedes darte de baja: tienes compras en curso que no han sido confirmadas.")
    
    # Validar contraofertas activas
    productos = get_productos_usuario(cn, username)
    for p in productos:
        contraofertas = consultar_contraofertas(cn, p['id_producto'])
        if len(contraofertas) > 0:
            raise ValueError(f"El producto '{p['titulo']}' tiene contraofertas activas. Debes resolverlas primero.")
        
    # Desactivar productos y ejecutar baja (Borrado lógico)
    for p in productos:
        if p.get("disponible"):
            eliminar_producto(cn, p['id_producto'], username)
    
    usuarios_repo.soft_delete_usuario(cn, username)


def get_usuario(cn, username: str) -> dict | None:
    """Obtiene un usuario por username.

    Args:
        cn: Conexión a la base de datos
        username: Nombre de usuario

    Returns:
        Dict con datos del usuario o None si no existe
    """
    return usuarios_repo.get_usuario(cn, username)


def get_categorias_disponibles(cn) -> list[str]:
    """Obtiene la lista de categorías disponibles de la base de datos.

    Args:
        cn: Conexión a la base de datos

    Returns:
        Lista de nombres de categorías
    """
    return usuarios_repo.get_categorias_disponibles(cn)


def get_categorias_preferidas(cn, username: str) -> list[str]:
    """Obtiene las categorías preferidas de un usuario.

    Args:
        cn: Conexión a la base de datos
        username: Nombre de usuario

    Returns:
        Lista de categorías preferidas del usuario
    """
    return usuarios_repo.get_categorias_preferidas(cn, username)


def update_saldo(cn, username: str, nuevo_saldo: float) -> None:
    """Actualiza el saldo del monedero del usuario.

    Args:
        cn: Conexión a la base de datos
        username: Usuario
        nuevo_saldo: Nuevo saldo del monedero
    """
    usuarios_repo.update_saldo(cn, username, nuevo_saldo)


def update_valoracion(cn, username: str, valoracion: float) -> None:
    """Actualiza la valoración media de un usuario.

    Args:
        cn: Conexión a la base de datos
        username: Usuario a actualizar
        valoracion: Nueva valoración media (0-5)
    """
    usuarios_repo.update_valoracion(cn, username, valoracion)
