"""
Repositorio de acceso a datos de usuarios.
Responsable: Eisa Rodríguez

Operaciones CRUD sobre la tabla USUARIO.
"""


def insert_usuario(cn, usuario: dict) -> None:
    """Inserta un nuevo usuario en la BD y sus categorías preferidas en Preferidos.
    
    Args:
        cn: Conexión a la base de datos
        usuario: Dict con todos los campos del usuario
    """
    # Campos esperados (service debe validar antes):
    username = usuario.get("username")
    correo = usuario.get("correo")
    nombre = usuario.get("nombre_completo")
    contrasenia = usuario.get("contraseña") or usuario.get("contrasenia")
    ubic = usuario.get("ubicacion")
    lat = lon = None
    if isinstance(ubic, (list, tuple)) and len(ubic) >= 2:
        try:
            lat = float(ubic[0]); lon = float(ubic[1])
        except Exception:
            lat = lon = None
    rango = usuario.get("rango")
    saldo = usuario.get("saldo", 0.0)
    valoracion_media = usuario.get("valoracion_media")
    cuenta_eliminada = 1 if usuario.get("cuenta_eliminada") else 0
    categorias = usuario.get("categorias", [])

    sql_usuario = (
        "INSERT INTO Usuario (username, correo, nombre_completo, contrasenia, "
        "ubi_latitud, ubi_longitud, rango, saldo, valoracion_media, cuenta_eliminada)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    
    sql_preferido = "INSERT INTO Preferidos (username, nombre) VALUES (?, ?)"

    # If caller did not provide a connection, open one using db_app.connect()
    if cn is None:
        from src.db.db_app import connect
        with connect() as local_cn:
            cur = local_cn.cursor()
            try:
                # Unicidad: comprobar username y correo
                cur.execute("SELECT username FROM Usuario WHERE username = ? OR correo = ?", (username, correo))
                if cur.fetchone():
                    raise ValueError("Nombre de usuario o correo ya existente")
                cur.execute(sql_usuario, (username, correo, nombre, contrasenia, lat, lon, rango, saldo, valoracion_media, cuenta_eliminada))
                # Insertar categorías preferidas
                for cat in categorias:
                    cur.execute(sql_preferido, (username, cat))
                local_cn.commit()
            except Exception as e:
                try:
                    local_cn.rollback()
                except Exception:
                    pass
                raise ValueError(f"Error insertando usuario: {e}")
            finally:
                cur.close()
        return

    # Use provided connection (DB-API compatible). Use savepoint + rollback_to_savepoint if available.
    from src.db.db_app import savepoint, rollback_to_savepoint
    sp_name = "SP_INSERT_USUARIO"
    try:
        savepoint(cn, sp_name)
    except Exception:
        # Driver may not support savepoints; continue
        pass

    cur = cn.cursor()
    try:
        cur.execute("SELECT username FROM Usuario WHERE username = ? OR correo = ?", (username, correo))
        if cur.fetchone():
            try:
                rollback_to_savepoint(cn, sp_name)
            except Exception:
                pass
            raise ValueError("Nombre de usuario o correo ya existente")
        cur.execute(sql_usuario, (username, correo, nombre, contrasenia, lat, lon, rango, saldo, valoracion_media, cuenta_eliminada))
        # Insertar categorías preferidas en tabla Preferidos
        for cat in categorias:
            cur.execute(sql_preferido, (username, cat))
        # Commit la transacción
        cn.commit()
    except Exception as e:
        try:
            rollback_to_savepoint(cn, sp_name)
        except Exception:
            pass
        raise ValueError(f"Error insertando usuario: {e}")
    finally:
        try:
            cur.close()
        except Exception:
            pass


def get_usuario(cn, username: str) -> dict | None:
    """Obtiene un usuario por username.
    
    Args:
        cn: Conexión a la base de datos
        username: Nombre de usuario
    
    Returns:
        Dict con datos del usuario o None si no existe
    """
    cur = cn.cursor()

    try:
        cur.execute(
            "SELECT username, correo, nombre_completo, contrasenia, "
            "ubi_latitud, ubi_longitud, rango, saldo, valoracion_media, cuenta_eliminada "
            "FROM Usuario WHERE username = ?",
            (username,)
        )
        row = cur.fetchone()
        if row is None:
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
    except Exception as e:
        print(f"Error obteniendo usuario {username}: {e}")
        return None
    finally:
        try:
            cur.close()
        except Exception:
            pass

def update_usuario(cn, username: str, cambios: dict) -> None:
    """Actualiza campos de un usuario.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario a actualizar
        cambios: Dict con campos a modificar
    
    Campos permitidos:
        - nombre_completo
        - correo
        - ubi_latitud, ubi_longitud (ubicación)
        - rango
    """
    # Campos permitidos a actualizar
    campos_permitidos = ["nombre_completo", "correo", "ubi_latitud", "ubi_longitud", "rango"]
    
    # Filtrar cambios a solo campos permitidos
    cambios_filtrados = {k: v for k, v in cambios.items() if k in campos_permitidos}
    
    if not cambios_filtrados:
        return
    
    # Construir SQL dinámico
    set_clause = ", ".join([f"{k} = ?" for k in cambios_filtrados.keys()])
    sql = f"UPDATE Usuario SET {set_clause} WHERE username = ?"
    
    values = list(cambios_filtrados.values()) + [username]
    
    cur = cn.cursor()
    try:
        cur.execute(sql, values)
        cn.commit()  # Commit the transaction to save changes
    finally:
        cur.close()


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
    cn.commit()  # Commit the transaction
    cur.close()


def soft_delete_usuario(cn, username: str) -> None:
    """Marca un usuario como eliminado (cuenta_eliminada = true).
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario a dar de baja
    """
    cur = cn.cursor()
    try:
        # Se conservan las claves (username), se limpian datos personales
        # y se marca cuenta_eliminada como true (1)
        cur.execute("""
            UPDATE Usuario 
            SET correo = '', 
                nombre_completo = 'Usuario Eliminado', 
                contrasenia = '********', 
                ubi_latitud = NULL, 
                ubi_longitud = NULL, 
                rango = NULL,
                saldo = 0,
                cuenta_eliminada = 1 
            WHERE username = ?
        """, (username,))
        
        # Opcional: Limpiar categorías preferidas
        cur.execute("DELETE FROM Preferidos WHERE username = ?", (username,))
        
        # Confirmar los cambios en la base de datos
        cn.commit()
    finally:
        cur.close()


def get_categorias_disponibles(cn) -> list[str]:
    """Obtiene la lista de categorías disponibles de la tabla Categoria.
    
    Args:
        cn: Conexión a la base de datos
    
    Returns:
        Lista de nombres de categorías
    """
    cur = cn.cursor()
    try:
        cur.execute("SELECT nombre FROM Categoria ORDER BY nombre")
        categorias = [row[0] for row in cur.fetchall()]
        return categorias
    except Exception as e:
        print(f"Error obteniendo categorías: {e}")
        return []
    finally:
        try:
            cur.close()
        except Exception:
            pass


def get_categorias_preferidas(cn, username: str) -> list[str]:
    """Obtiene las categorías preferidas de un usuario.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
    
    Returns:
        Lista de nombres de categorías preferidas
    """
    cur = cn.cursor()
    try:
        cur.execute(
            "SELECT nombre FROM Preferidos WHERE username = ? ORDER BY nombre",
            (username,)
        )
        categorias = [row[0] for row in cur.fetchall()]
        return categorias
    except Exception as e:
        print(f"Error obteniendo categorías preferidas: {e}")
        return []
    finally:
        try:
            cur.close()
        except Exception:
            pass


def update_categorias_preferidas(cn, username: str, categorias: list[str]) -> None:
    """Actualiza las categorías preferidas de un usuario.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        categorias: Lista de categorías (debe tener entre 1 y 6 elementos)
    """
    if not categorias or len(categorias) > 6:
        raise ValueError("Las categorías preferidas deben ser entre 1 y 6")
    
    cur = cn.cursor()
    try:
        # Eliminar categorías previas
        cur.execute("DELETE FROM Preferidos WHERE username = ?", (username,))
        cn.commit()  # Commit the deletion

        # Insertar nuevas categorías
        for cat in categorias:
            cur.execute(
                "INSERT INTO Preferidos (username, nombre) VALUES (?, ?)",
                (username, cat)
            )
        cn.commit()  # Commit the insertion
    finally:
        cur.close()


def verificar_contraseña(cn, username: str, contraseña: str) -> bool:
    """Verifica si la contraseña es correcta.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        contraseña: Contraseña a verificar
    
    Returns:
        True si coincide, False si no
    """
    if not username or not contraseña:
        return False
    
    cur = cn.cursor()
    try:
        cur.execute(
            "SELECT contrasenia FROM Usuario WHERE username = ?",
            (username,)
        )
        row = cur.fetchone()
        if row is None:
            return False
        
        contraseña_bd = row[0]
        # Comparación de texto plano (sin hash, como indicó el usuario)
        return contraseña_bd == contraseña
    except Exception as e:
        print(f"Error verificando contraseña para {username}: {e}")
        return False
    finally:
        try:
            cur.close()
        except Exception:
            pass


def obtener_ventas_como_comprador(cn, username: str) -> list[dict]:
    """
    Obtiene las ventas activas como comprador para un usuario.

    Args:
        cn: Conexión a la base de datos
        username: Nombre de usuario

    Returns:
        Una lista de diccionarios con las ventas activas como comprador.
    """
    cursor = cn.cursor()
    query = """
        SELECT v.*
        FROM Vendido v
        WHERE v.username = ? AND v.recepcion_confirmada = 0
    """
    cursor.execute(query, (username,))
    ventas = cursor.fetchall()
    return [dict(zip([column[0] for column in cursor.description], row)) for row in ventas]
