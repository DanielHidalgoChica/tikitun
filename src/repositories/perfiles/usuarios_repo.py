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
    if not username:
        return None
    
    cur = cn.cursor()
    cur.execute("""
        SELECT 
            username,
            correo,
            nombre_completo,
            contrasenia,
            ubi_latitud,
            ubi_longitud,
            rango,
            saldo,
            valoracion_media,
            cuenta_eliminada
        FROM Usuario
        WHERE username = ?
    """, (username,))
    
    row = cur.fetchone()
    cur.close()
    
    if not row:
        return None
    
    return {
        "username": row[0],
        "correo": row[1],
        "nombre_completo": row[2],
        "contrasenia": row[3],
        "ubi_latitud": row[4],
        "ubi_longitud": row[5],
        "rango": row[6],
        "saldo": row[7] if row[7] is not None else 0.0,
        "valoracion_media": row[8],
        "cuenta_eliminada": bool(row[9]) if row[9] is not None else False
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
    cur = cn.cursor()
    cur.execute("""
        UPDATE Usuario
        SET saldo = ?
        WHERE username = ?
    """, (nuevo_saldo, username))
    cur.close()


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
