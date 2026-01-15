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


def realizar_compra_directa(cn, id_producto: int, username_comprador: str) -> None:
    """RF4.1: Compra directa de un producto al precio establecido.
    
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
    """
    print(" [SERVICE ventas] realizar_compra_directa()")
    # TODO: Implementar
    pass


def realizar_contraoferta(cn, id_producto: int, username_comprador: str, 
                         precio_oferta: float) -> None:
    """RF4.2: Realiza una contraoferta por un producto.
    
    RS aplicadas:
    - Precio oferta < precio producto
    - Precio oferta ≤ saldo comprador
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador que hace la oferta
        precio_oferta: Precio propuesto
    
    Raises:
        ValueError: Si oferta no viable
    """
    print(" [SERVICE ventas] realizar_contraoferta()")
    # TODO: Validar precio < precio_producto
    # TODO: Validar precio <= saldo_comprador
    # TODO: contraofertas_repo.insert_contraoferta(...)
    pass


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
    # TODO: Obtener contraoferta
    # TODO: Ejecutar compra con precio de contraoferta
    # TODO: Eliminar contraoferta
    pass


def rechazar_contraoferta(cn, id_producto: int, username_comprador: str) -> None:
    """RF4.3: Vendedor rechaza una contraoferta.
    
    Args:
        cn: Conexión a la base de datos
        id_producto: Producto
        username_comprador: Comprador de la contraoferta
    """
    print(" [SERVICE ventas] rechazar_contraoferta()")
    # TODO: contraofertas_repo.delete_contraoferta(...)
    pass


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
    # TODO: Actualizar estado_recepcion = true
    # TODO: Transferir saldo al vendedor
    pass


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
    print(" [SERVICE ventas] puntuar_venta()")
    # TODO: Validar puntuación en {0, 0.5, 1, ..., 5}
    # TODO: Actualizar valoracion_media del vendedor
    pass
