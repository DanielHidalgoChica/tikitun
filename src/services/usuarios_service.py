from src.repositories import usuarios_repo

def obtener_usuario(cn, username: str) -> dict:
    print(" [SERVICE usuarios] obtener_usuario()")
    u = usuarios_repo.get_usuario(cn, username)
    if u is None:
        raise ValueError("Usuario no existe.")
    return u
