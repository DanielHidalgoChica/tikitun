"""
Repositorio de acceso a datos de conversaciones.
Responsable: Aitor de la Iglesia

Operaciones sobre la tabla CONVERSACION.
"""

def _get_next_id_chat(cn) -> int:
    """Obtiene el siguiente ID disponible para un chat.
    
    Oracle no tiene AUTOINCREMENT, así que usamos MAX(id_chat) + 1.
    """
    cur = cn.cursor()
    cur.execute("SELECT COALESCE(MAX(id_chat), 0) + 1 FROM Chat")
    row = cur.fetchone()
    cur.close()
    return row[0] if row else 1

def puede_crear_conversacion(cn, username: str, id_producto: int) -> bool:
    """
    Comprueba si un usuario puede crear una conversación sobre un producto.

    Reglas:
    - No se puede si el producto pertenece al propio usuario
    - No se puede si ya existe una conversación entre ese usuario y ese producto
    """
    sql = """
    SELECT
        p.username AS vendedor,
        COUNT(c.id_chat) AS chats_existentes
    FROM Producto p
    LEFT JOIN Chat c 
        ON c.id_producto = p.id_producto
       AND c.username = :username
    WHERE p.id_producto = :id_producto
    GROUP BY p.username
    """

    cur = cn.cursor()
    cur.execute(sql, {"username": username, "id_producto": id_producto})
    row = cur.fetchone()
    cur.close()

    if not row:
        raise ValueError("El producto no existe")

    vendedor, chats = row

    if vendedor == username:
        return False   # es tu propio producto

    if chats > 0:
        return False   # ya hay chat creado

    return True

def crear_conversacion(cn, username: str, id_producto: int) -> None:
    """
    Crea un nuevo chat
    """
    cur = cn.cursor()
    cur.execute("""
                INSERT INTO Chat (id_chat, id_producto, username, archivado)
                VALUES (:1,:2,:3,:4)
                """, (_get_next_id_chat(cn), id_producto, username, 0))
    cur.close()
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
