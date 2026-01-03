from src.db.db_app import savepoint
from src.repositories import chats_repo, usuarios_repo

def abrir_chat(cn, data: dict) -> int:
    print(" [SERVICE chats] abrir_chat()")

    comprador = data.get("username_comprador", "")
    vendedor = data.get("username_vendedor", "")

    # TODO RS: comprador != vendedor, usuarios existen, producto existe, etc.
    if comprador == vendedor:
        raise ValueError("No puedes abrir chat contigo mismo.")

    if usuarios_repo.get_usuario(cn, comprador) is None:
        raise ValueError("Comprador no existe.")
    if usuarios_repo.get_usuario(cn, vendedor) is None:
        raise ValueError("Vendedor no existe.")

    savepoint(cn, "SP_ABRIR_CHAT")
    return chats_repo.create_chat(cn, data)
