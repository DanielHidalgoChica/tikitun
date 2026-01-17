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
    Returns:
        usuario receptor
    """
    print("   [REPO mensajes] insert_mensaje()", mensaje)
    sql = """
        INSERT INTO Mensaje (id_chat, fecha, username, texto, adjunto, leido)
        VALUES (:1, SYSTIMESTAMP, :2, :3, :4, :5)
    """
    cur = cn.cursor()
    cur.execute(sql, (mensaje["id_chat"],mensaje["emisor"],mensaje["texto"],mensaje.get("adjunto"),0))
    cur.close()
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
        SELECT username, texto, fecha, adjunto, leido
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
    sql = """
        SELECT m.id_chat, m.username, m.texto, m.fecha, p.titulo
        FROM Mensaje m
        JOIN Chat c ON m.id_chat = c.id_chat
        JOIN Producto p ON c.id_producto = p.id_producto
        WHERE (c.username = :u OR p.username = :u)
    """
    params = [username, username]

    if filtros.get("usuario"):
        sql += " AND m.username = :usuario"
        params.append(filtros["usuario"])

    if filtros.get("texto"):
        sql += " AND LOWER(m.texto) LIKE :texto"
        params.append(f"%{filtros['texto'].lower()}%")

    if filtros.get("fecha"):
        sql += " AND TRUNC(m.fecha) = TO_DATE(:fecha, 'YYYY-MM-DD')"
        params.append(filtros["fecha"])

    if not filtros["incluir_archivados"]:
        sql += " AND c.archivado = 0"
        
    sql += " ORDER BY m.fecha DESC"

    cur = cn.cursor()
    cur.execute(sql, params)
    cols = [c[0].lower() for c in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    cur.close()
    return rows
