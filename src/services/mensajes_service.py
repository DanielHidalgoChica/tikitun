from src.db.db_app import savepoint
from src.repositories import mensajes_repo

def enviar_mensaje(cn, data: dict) -> int:
    print(" [SERVICE mensajes] enviar_mensaje()")

    # TODO RS: chat existe, emisor pertenece al chat, mensaje no vacío, etc.
    if not data.get("texto"):
        raise ValueError("El mensaje no puede estar vacío.")

    savepoint(cn, "SP_ENVIAR_MENSAJE")
    return mensajes_repo.insert_mensaje(cn, data)
