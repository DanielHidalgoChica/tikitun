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
    # TODO: Implementar
    pass


def modificar_perfil(cn, username: str, cambios: dict) -> None:
    """RF1.3: Modifica datos del perfil de usuario.
    
    RS aplicadas:
    - RS1.3: Nombre de usuario y correo únicos
    - RS1.7: Entre 1 y 6 categorías de preferencia
    - RS1.13: Usuario debe existir y no estar eliminado
    - RS1.18: Rango de interés positivo
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario a modificar
        cambios: Dict con campos a actualizar
    
    Raises:
        ValueError: Si no cumple validaciones
    """
    print(" [SERVICE perfiles] modificar_perfil()")
    # TODO: Implementar validaciones y actualización
    pass


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
    # TODO: Implementar validaciones
    # TODO: savepoint(cn, "SP_AÑADIR_SALDO")
    # TODO: usuarios_repo.update_saldo(cn, username, nuevo_saldo)
    pass


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
    # TODO: Implementar validaciones
    # TODO: savepoint(cn, "SP_TRANSFERIR_SALDO")
    pass


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
    print(" [SERVICE perfiles] dar_baja_usuario()")
    # TODO: Verificar que no tiene ventas activas
    # TODO: Marcar cuenta_eliminada = true
    # TODO: Marcar productos como no disponibles
    pass
