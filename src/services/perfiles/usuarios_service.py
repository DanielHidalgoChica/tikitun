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
    print(" [SERVICE perfiles] dar_alta_usuario()")
    # TODO: Implementar validaciones RS
    # TODO: Llamar a usuarios_repo.insert_usuario(cn, data)
    pass


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
