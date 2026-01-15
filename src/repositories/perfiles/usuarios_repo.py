"""
Repositorio de acceso a datos de usuarios.
Responsable: Eisa Rodríguez

Operaciones CRUD sobre la tabla USUARIO.
"""


def insert_usuario(cn, usuario: dict) -> None:
    """Inserta un nuevo usuario en la BD.
    
    Args:
        cn: Conexión a la base de datos
        usuario: Dict con todos los campos del usuario
    """
    print("   [REPO perfiles] insert_usuario()", usuario)
    # TODO: INSERT INTO USUARIO (...) VALUES (...)
    pass


def get_usuario(cn, username: str) -> dict | None:
    """Obtiene un usuario por username.
    
    Args:
        cn: Conexión a la base de datos
        username: Nombre de usuario
    
    Returns:
        Dict con datos del usuario o None si no existe
    """
    print("   [REPO perfiles] get_usuario()", username)
    # TODO: SELECT * FROM USUARIO WHERE username = ?
    
    # Demo (eliminar cuando implementes)
    if not username:
        return None
    return {
        "username": username,
        "saldo": 100.00,
        "nombre_completo": "Usuario Demo",
        "cuenta_eliminada": False
    }


def update_usuario(cn, username: str, cambios: dict) -> None:
    """Actualiza campos de un usuario.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario a actualizar
        cambios: Dict con campos a modificar
    """
    print("   [REPO perfiles] update_usuario()", username, cambios)
    # TODO: UPDATE USUARIO SET ... WHERE username = ?
    pass


def update_saldo(cn, username: str, nuevo_saldo: float) -> None:
    """Actualiza el saldo del monedero.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        nuevo_saldo: Nuevo saldo del monedero
    """
    print("   [REPO perfiles] update_saldo()", username, nuevo_saldo)
    # TODO: UPDATE USUARIO SET saldo = ? WHERE username = ?
    pass


def soft_delete_usuario(cn, username: str) -> None:
    """Marca un usuario como eliminado (cuenta_eliminada = true).
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario a dar de baja
    """
    print("   [REPO perfiles] soft_delete_usuario()", username)
    # TODO: UPDATE USUARIO SET cuenta_eliminada = true, ... WHERE username = ?
    pass


def verificar_contraseña(cn, username: str, contraseña: str) -> bool:
    """Verifica si la contraseña es correcta.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        contraseña: Contraseña a verificar
    
    Returns:
        True si coincide, False si no
    """
    print("   [REPO perfiles] verificar_contraseña()", username)
    # TODO: SELECT contraseña FROM USUARIO WHERE username = ?
    # TODO: Comparar hash (si usas hash) o texto plano
    return True  # Demo
