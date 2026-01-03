def get_usuario(cn, username: str) -> dict | None:
    print("   [REPO usuarios] get_usuario()", username)
    # TODO: SELECT ... FROM Usuario WHERE username = :username
    if username.strip() == "":
        return None
    return {"username": username, "saldo": 999}
