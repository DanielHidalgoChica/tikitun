"""
Repositorio de acceso a datos de conversaciones.
Responsable: Aitor de la Iglesia

Operaciones sobre la tabla CONVERSACION.
"""

def crear_conversacion(cn, username: str, id_producto: int) -> None:
    pass

def get_conversaciones_usuario(cn, username: str) -> list[dict]:
    """Obtiene todas las conversaciones del usuario.
    
    Args:
        cn: Conexión a la base de datos
        username: Usuario
    
    Returns:
        Lista de conversaciones (como comprador o vendedor)
    """
    print("   [REPO conversaciones] get_conversaciones_usuario()", username)

    sql = """
        SELECT 
        c.id_chat,
        c.id_producto,
        c.username        AS comprador,
        p.username        AS vendedor,
        p.titulo,
        c.archivado
        FROM Chat c JOIN Producto p ON c.id_producto = p.id_producto 
        WHERE c.username = :1 or p.username = :2
        ORDER BY c.archivado asc;
        """
    cur = cn.cursor()
    try:
        cur.execute(sql, (username, username))
        cols = [c[0].lower() for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    except Exception as e:
        raise
    cur.close()
    return rows


def set_archivada(cn, id_producto: int, archivada: bool) -> None:
    """Marca una conversación como archivada.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto de la conversación
        archivada: True para archivar
    """
    print("   [REPO conversaciones] set_archivada()", id_producto, archivada)
    # TODO: UPDATE CONVERSACION SET archivada = ? WHERE id_producto = ?
    pass

def get_receptor_mensaje(cn, id_chat: int, emisor: str) -> str:
    """
    Dado un chat y el emisor, devuelve el username del receptor.
    """
    print("   [REPO conversaciones] get_receptor_chat()", id_chat, emisor)

    sql = """
        SELECT
            CASE
                WHEN c.username = :1 THEN p.username
                ELSE c.username
            END AS receptor
        FROM Chat c
        JOIN Producto p ON c.id_producto = p.id_producto
        WHERE c.id_chat = :2
    """
    cur = cn.cursor()
    try:
        cur.execute(sql, (emisor, id_chat))
        row = cur.fetchone()
        if not row:
            return None
        return row[0]
    finally:
        cur.close()
