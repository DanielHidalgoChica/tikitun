from src.db.db_app import savepoint
from src.repositories import productos_repo

def publicar_producto(cn, data: dict) -> int:
    print(" [SERVICE productos] publicar_producto()")

    # TODO RS: precio > 0, titulo no vacío, vendedor existe, etc.
    if not data.get("titulo"):
        raise ValueError("El título no puede estar vacío.")
    if float(data.get("precio", 0)) <= 0:
        raise ValueError("El precio debe ser mayor que 0.")

    savepoint(cn, "SP_PUBLICAR_PRODUCTO")
    new_id = productos_repo.insert_producto(cn, data)
    return new_id

def buscar_productos(cn, filtros: dict) -> list[dict]:
    print(" [SERVICE productos] buscar_productos()")
    return productos_repo.search_productos(cn, filtros)
