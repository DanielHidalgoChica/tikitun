"""
Repositorio de acceso a datos de mensajes.
Responsable: Aitor de la Iglesia

Operaciones sobre la tabla MENSAJE.
"""

def ultimo_mensaje(cn, id_chat: int) -> dict | None:
    """
    Devuelve el último mensaje de la conversación
    
    Args:
        cn: Conexión a la base de datos
        id_chat: ID del chat
    
    Returns:
        Ultimo mensaje de la conversación
    """
    sql = """
        SELECT texto, fecha, username
        FROM Mensaje
        WHERE id_chat = :1
        ORDER BY fecha DESC
        FETCH FIRST 1 ROW ONLY
    """
    cur = cn.cursor()
    cur.execute(sql, (id_chat))
    row = cur.fetchone()
    if not row:
        return None
    cur.close()
    return {
        "texto": row[0],
        "fecha": row[1],
        "autor": row[2]
    }

def insert_mensaje(cn, mensaje: dict) -> None:
    """Inserta un nuevo mensaje.
    
    Args:
        cn: Conexión a la base de datos
        mensaje: Dict con todos los campos del mensaje
    """
    print("   [REPO mensajes] insert_mensaje()", mensaje)
    # TODO: INSERT INTO MENSAJE (...) VALUES (...)
    pass


def get_mensajes_conversacion(cn, username: str, id_chat: int) -> list[dict]:
    """Obtiene todos los mensajes de una conversación.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador
        username_vendedor: Vendedor
    
    Returns:
        Lista de mensajes ordenados por fecha
    """
    print("   [REPO mensajes] get_mensajes_conversacion()", id_chat)
    sql = """
        SELECT username, texto, fecha, leido
        FROM Mensaje
        WHERE id_chat = :1
        ORDER BY fecha ASC
        """
    cur = cn.cursor()
    cur.execute(sql, (id_chat))

    cols = [c[0].lower() for c in cur.description]
    rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def mark_as_read(cn, id_chat: int, username: str) -> None:
    """Marca mensajes como leídos.
    
    Args:
        cn: Conexión a la base de datos
        id_chat
        username
    """
    print("   [REPO mensajes] mark_as_read()",id_chat,username)
    sql = """
        UPDATE Mensaje
        SET leido = 1
        WHERE id_chat = :1
        AND username <> :2
        AND leido = 0
    """
    cur = cn.cursor()
    print('hola')
    try:
        cur.execute(sql, (id_chat, username))
    finally:
        cur.close()
    print('adios')
    pass


def search_mensajes(cn, username: str, filtros: dict) -> list[dict]:
    """Busca mensajes según filtros.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
        filtros: Dict con palabras_clave, usuario, fecha
    
    Returns:
        Mensajes que coinciden
    """
    print("   [REPO mensajes] search_mensajes()", username, filtros)
    # TODO: SELECT con WHERE y LIKE para búsqueda
    return []
