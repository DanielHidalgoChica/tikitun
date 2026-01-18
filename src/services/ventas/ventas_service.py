"""
Servicios de gestión de ventas.
Responsable: Juan Manuel Fernández

Requisitos Funcionales implementados:
- RF4.1: Realizar compra directa de producto
- RF4.2: Realizar contraoferta de producto
- RF4.3: Aceptar/Rechazar contraoferta
- RF4.4: Consultar contraofertas asociadas a producto
- RF4.5: Confirmación compra del producto
- RF4.6: Puntuar compra del producto
"""

from src.db.db_app import savepoint
from src.repositories.ventas import ventas_repo, contraofertas_repo
from src.services.productos import productos_service
from src.services.perfiles import usuarios_service


def realizar_compra_directa(cn, id_producto: int, username_comprador: str) -> None:
    """RF4.1: Compra directa de un producto al precio establecido.
    
    RS aplicadas:
    - El comprador no es dueño del producto id_producto
    - Saldo comprado >= precio producto

    Flujo:
    1. Verificar saldo suficiente
    2. Retirar dinero del monedero del comprador
    3. Crear registro de venta (estado pendiente recepción)
    4. Marcar producto como no disponible
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto a comprar
        username_comprador: Comprador
    
    Raises:
        ValueError: Si saldo insuficiente o producto no disponible
        ValueError: Si el propietario del producto es el comprador
    """
    print(" [SERVICE ventas] realizar_compra_directa()")

    # Validación restricciones semánticas
    comprador = usuarios_service.get_usuario(cn, username_comprador)
    if not comprador:
        raise ValueError("El usuario no existe")

    producto = productos_service.consultar_producto(cn, id_producto)
    if not producto:
        raise ValueError("El producto no existe")

    saldo_comprador = comprador['saldo']
    precio = producto['precio']

    if (precio > saldo_comprador):
        raise ValueError("No hay saldo suficiente para realizar la compra")
    
    propietario = producto['username_vendedor']
    if (username_comprador == propietario):
        raise ValueError("El propietario no puede realizar contraofertas a sus propios productos")
    
    # Retirar dinero del comprador.
    usuarios_service.update_saldo(cn, username_comprador, saldo_comprador-precio)

    # Crear registro de venta
    venta = dict([
        ('id_producto', id_producto),
        ('username' , username_comprador),
        ('recepcion_confirmada' , 0),
        ('precio_final', precio),
        ('valoracion', 0)
    ])
    ventas_repo.insert_venta(cn, venta)

    # Marcar producto como no disponible
    productos_service.eliminar_producto(cn, id_producto, propietario)


def realizar_contraoferta(cn, id_producto: int, username_comprador: str, 
                         precio_oferta: float) -> None:
    """RF4.2: Realiza una contraoferta por un producto.
    
    RS aplicadas:
    - Precio oferta < precio producto
    - Precio oferta ≤ saldo comprador
    - El comprador no es dueño del producto id_producto
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador que hace la oferta
        precio_oferta: Precio propuesto
    
    Raises:
        ValueError: Si oferta no viable
    """
    print(" [SERVICE ventas] realizar_contraoferta()")
    
    # Validación de las restricciones semánticas
    prod = productos_service.consultar_producto(cn, id_producto)
    if not prod:
        raise ValueError("El producto no existe")
    
    comprador = usuarios_service.get_usuario(cn, username_comprador)
    if not comprador:
        raise ValueError("El usuario no existe")

    precio = prod['precio']
    propietario = prod['username_vendedor']

    if (username_comprador == propietario):
        raise ValueError("El propietario no puede realizar contraofertas a sus propios productos")
    
    if ((precio_oferta >= precio) or (precio_oferta < 0)):
        raise ValueError("El precio de la contraoferta es incorrecto")
    
    # Crear la contraoferta
    contraoferta = dict([
        ('id_producto', id_producto),
        ('username', username_comprador),
        ('precio', precio_oferta)
    ])

    contraofertas_repo.insert_contraoferta(cn, contraoferta)


def aceptar_contraoferta(cn, id_producto: int, username_comprador: str,
                        username_vendedor: str) -> None:
    """RF4.3: Vendedor acepta una contraoferta.
    
    Flujo similar a compra directa pero con precio de contraoferta.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador de la contraoferta
        username_vendedor: Vendedor que acepta
    """
    print(" [SERVICE ventas] aceptar_contraoferta()")

    # Validación restricciones semánticas
    comprador = usuarios_service.get_usuario(cn, username_comprador)
    if not comprador:
        raise ValueError("El usuario comprador no existe")
    
    vendedor = usuarios_service.get_usuario(cn, username_vendedor)
    if not vendedor:
        raise ValueError("El usuario vendedor no existe")

    producto = productos_service.consultar_producto(cn, id_producto)
    if not producto:
        raise ValueError("El producto no existe")
    
    propietario = producto['username_vendedor']

    if (username_vendedor != propietario):
        raise ValueError("El vendedor no es el propietario del producto")
    
    if (username_comprador == username_vendedor):
        raise ValueError("El propietario no puede realizar contraofertas a sus propios productos")
    
    contraoferta = contraofertas_repo.get_contraoferta(cn, id_producto, username_comprador)
    precio = contraoferta['precio']
    saldo_comprador = comprador['saldo']
    
    # Retirar dinero del comprador.
    usuarios_service.update_saldo(cn, username_comprador, saldo_comprador-precio)

    # Crear registro de venta y eliminar la contraoferta
    venta = dict([
        ('id_producto', id_producto),
        ('username' , username_comprador),
        ('recepcion_confirmada' , 0),
        ('precio_final', precio),
        ('valoracion', 0)
    ])

    contraofertas_repo.delete_contraoferta(cn, id_producto, username_comprador)
    ventas_repo.insert_venta(cn, venta)

    # Marcar producto como no disponible
    productos_service.eliminar_producto(cn, id_producto, propietario)


def rechazar_contraoferta(cn, id_producto: int, username_comprador: str) -> None:
    """RF4.3: Vendedor rechaza una contraoferta.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador de la contraoferta
    """
    print(" [SERVICE ventas] rechazar_contraoferta()")
    contraofertas_repo.delete_contraoferta(cn, id_producto, username_comprador)

def consultar_contraofertas(cn, id_producto: int) -> list[dict]:
    """RF4.4: Obtiene todas las contraofertas de un producto.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
    
    Returns:
        Lista de contraofertas con username_comprador y precio
    """
    print(" [SERVICE ventas] consultar_contraofertas()")
    return contraofertas_repo.get_contraofertas(cn, id_producto)


def confirmar_recepcion(cn, id_producto: int, username_comprador: str) -> None:
    """RF4.5: Comprador confirma que ha recibido el producto.
    
    Flujo:
    1. Marcar venta como recibida
    2. Transferir dinero al vendedor
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador que confirma
    """
    print(" [SERVICE ventas] confirmar_recepcion()")

    ventas_repo.update_estado_recepcion(cn, id_producto, 1)

    venta = ventas_repo.get_venta(cn, id_producto)
    producto = productos_service.consultar_producto(cn, id_producto)
    vendedor = usuarios_service.get_usuario(cn, producto['username_vendedor'])

    usuarios_service.update_saldo(cn, vendedor, vendedor['saldo']+venta['precio_final'])


def puntuar_venta(cn, id_producto: int, puntuacion: float) -> None:
    """RF4.6: Comprador puntúa al vendedor tras la compra.
    
    Puntuación: 0 a 5 en saltos de 0.5
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto comprado
        puntuacion: Puntuación (0, 0.5, 1, ..., 5)
    
    Raises:
        ValueError: Si puntuación no válida
    """

    puntuaciones_validas = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]

    print(" [SERVICE ventas] puntuar_venta()")

    if (puntuacion not in puntuaciones_validas):
        raise ValueError("La puntuación es incorrecta. Las puntuaciones válidas van de 0 a 5 con saltos de 0.5")

    # Actualizar puntuación en la venta
    ventas_repo.update_puntuacion_venta(cn, id_producto, puntuacion)
    
    # Actualizar valoración media del vendedor
    producto = productos_service.consultar_producto(cn, id_producto)
    username_vendedor = producto['username']
    ventas_vendedor = ventas_repo.get_ventas_usuario(cn, username_vendedor)

    vendedor = usuarios_service.get_usuario(cn, username_vendedor)
    num_ventas = len(ventas_vendedor)
    valoracion_media = 0

    if(num_ventas == 0):
        valoracion_media = puntuacion
    else:
        valoracion_media = ((num_ventas*vendedor['valoracion_media'])+puntuacion)/(num_ventas+1)
    
    vendedor['valoracion_media']=valoracion_media
    usuarios_service.update_saldo(cn, vendedor)

def obtener_ventas_usuario(cn, username : str) -> list[dict]:
    """Devuelve todas las ventas asociadas a productos del usuario.

    Args:
        cn: Conexión a la base de datos
        username: Comprador
    
    Returns:
        Lista de ventas
    """
    return ventas_repo.get_ventas_usuario(cn, username)

def obtener_productos_comprados(cn, username : str) -> list[dict]:
    """
    Devuelve los productos comprados por el usuario.

    Args:
        cn: Conexión a la base de datos
        username: Comprador
    
    Returns:
        Lista de productos
    """
    return ventas_repo.get_productos_comprados(cn, username)

def eliminar_contraofertas(cn, username : str):
    productos = usuarios_service.get_productos_usuario(cn, username)

    id_productos = [prod["id_producto"] for prod in productos]

    for id in id_productos:
        contraofertas_repo.delete_contraoferta(cn, id, username)


def obtener_ventas_como_comprador(cn, username : str) -> list[dict]:
    """Devuelve todas las ventas asociadas a productos del usuario.

    Args:
        cn: Conexión a la base de datos
        username: Comprador
    
    Returns:
        Lista de ventas
    """
    return ventas_repo.get_ventas_como_comprador(cn, username)