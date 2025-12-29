# ------------------------------------------------------------
# db_app.py  —  Capa de acceso a datos para el Seminario
# ------------------------------------------------------------
import os
import pyodbc
from contextlib import contextmanager
from typing import Iterable, Sequence, Optional
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# --- Configuración desde .env ---
ORACLE_HOST = os.getenv("ORACLE_HOST", "oracle0.ugr.es")
ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE", "practbd")
ORACLE_USER = os.getenv("ORACLE_USER", "")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")

# (Opcional) nombre exacto del driver ODBC. Si no se define, intentaremos detectar uno.
ORACLE_ODBC_DRIVER = os.getenv("ORACLE_ODBC_DRIVER", "").strip()


def _find_oracle_driver() -> str:
    """Detecta un driver ODBC de Oracle entre los instalados.
    Prioriza el valor de ORACLE_ODBC_DRIVER si está definido."""
    if ORACLE_ODBC_DRIVER:
        return ORACLE_ODBC_DRIVER
    candidates = [d for d in pyodbc.drivers() if "oracle" in d.lower()]
    if not candidates:
        raise RuntimeError(
            "No se encontró un driver ODBC de Oracle. "
            "Define ORACLE_ODBC_DRIVER en .env o instala Oracle Instant Client ODBC."
        )
    # Preferir el último (suele ser el más reciente)
    return candidates[-1]


def _connect_string(driver: str) -> str:
    # Usamos formato driverless con DBQ=//host:port/service
    return (
        f"DRIVER={{{driver}}};"
        f"DBQ=//{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE};"
        f"UID={ORACLE_USER};PWD={ORACLE_PASSWORD};"
    )


@contextmanager  #Decorador 
def connect(autocommit: bool = False):
    #Todo esto se hace antes del bloque with en el que se llama
    """Abre una conexión ODBC a Oracle (por defecto autocommit=False)."""
    driver = _find_oracle_driver()
    cn = pyodbc.connect(_connect_string(driver), autocommit=autocommit, timeout=5)
    try:
        yield cn    #Aqui se abre el recurso que haya con with (Se ejecuta lo que haya en el bloque with)
    finally:
        cn.close()  #Esto se hace despues del bloque with en el que se llame


# --------------------------------------------------------------------
# Utilidades mínimas para el seminario (tablas, consultas y transacción)
# Esquema: Stock(Cproducto, Cantidad)
#          Pedido(Cpedido, Ccliente, Fecha_pedido)
#          Detalle_Pedido(Cpedido, Cproducto, Cantidad)
# --------------------------------------------------------------------
SEED_STOCK = [
    (1, 50),
    (2, 120),
    (3, 75),
    (4, 30),
    (5, 10),
    (6, 95),
    (7, 44),
    (8, 60),
    (9, 15),
    (10, 200),
]


def reset_schema() -> None:
    #Borra (si existen), crea las tablas del seminario y mete 10 filas en STOCK.
    ddl = [ 
        "DROP TABLE DETALLE_PEDIDO CASCADE CONSTRAINTS",
        "DROP TABLE PEDIDO CASCADE CONSTRAINTS",
        "DROP TABLE STOCK CASCADE CONSTRAINTS"
    ]
    create = [
        """
        CREATE TABLE STOCK (
            CPRODUCTO NUMBER PRIMARY KEY,
            CANTIDAD  NUMBER NOT NULL
        )
        """,
        """
        CREATE TABLE PEDIDO (
            CPEDIDO       NUMBER PRIMARY KEY,
            CCLIENTE      NUMBER NOT NULL,
            FECHA_PEDIDO  DATE   NOT NULL
        )
        """,
        """
        CREATE TABLE DETALLE_PEDIDO (
            CPEDIDO   NUMBER NOT NULL,
            CPRODUCTO NUMBER NOT NULL,
            CANTIDAD  NUMBER NOT NULL,
            CONSTRAINT PK_DETALLE PRIMARY KEY (CPEDIDO, CPRODUCTO),
            CONSTRAINT FK_DP_PEDIDO  FOREIGN KEY (CPEDIDO)   REFERENCES PEDIDO(CPEDIDO),
            CONSTRAINT FK_DP_STOCK   FOREIGN KEY (CPRODUCTO) REFERENCES STOCK(CPRODUCTO)
        )
        """,
    ]
    with connect(autocommit=False) as cn:
        cur = cn.cursor()
        # DROP tolerante
        for stmt in ddl:
            try:
                cur.execute(stmt)
            except pyodbc.Error as e:
                if "ORA-00942" not in str(e):  # table or view does not exist
                    raise
        # CREATE
        for stmt in create:
            cur.execute(stmt)
        # Seed STOCK
        cur.executemany(
            "INSERT INTO STOCK (CPRODUCTO, CANTIDAD) VALUES (?, ?)",
            SEED_STOCK,
        )
        cn.commit()
        cur.close()


def fetch_all_tables(cn: Optional[pyodbc.Connection] = None) -> dict:  #Key = Db name, Value = Dbs cells
    """Devuelve diccionario {tabla: [filas como dict]}.
    Si no se pasa conexión, abre una lectura propia (autocommit=False)."""
    owns = False
    if cn is None:
        owns = True
        cn_mgr = connect(autocommit=False)
        cn = cn_mgr.__enter__()             #Crea una conexion propia a mano para poder cerrarla después

    try:
        cur = cn.cursor()       #Seleccionamos un cursor (lo que permite ejecutar sentencias SQL a efectos prácticos)
        
        # Mostrar solo tablas de interés y en orden
        tables = ["STOCK", "PEDIDO", "DETALLE_PEDIDO"] #Futuras keys del dict de salida
        out = {}
        for t in tables:
            try:

                #Para cada tabla, hace SELECT * from tablaX
                #Al ejecutar algo en el cursor, se guarda "ahí" y luego se recupera con fetchall
                cur.execute(f"SELECT * FROM {t}")   
                
                #El primer elemento de la tupla de cur.description es el nombre de la columna (atributo en la tabla)
                #cur.description=[(name1, type_code1, display_size1, internal_size1, precision1, scale1, null_ok1),(...),...]
                cols = [c[0] for c in cur.description]

                #cur.fetchall devuelve una lista de tuplas con las filas de cada tabla
                #Cada tupla tiene los valores de cada columna en orden
                #Hacemos zip para emparejar cada columna con su valor en la fila (elemento 0 de la primera, 0 de la segunda, etc)
                    #[(0,a),(1,b),(2,c)] si cols = [0,1,2] y r = (a,b,c)
                #Y dict para convertir la lista en un diccionario, donde los pares son (clave: valor)
                rows = [dict(zip(cols, r)) for r in cur.fetchall()]

                #Por ejemplo, para la tabla PEDIDO, out['PEDIDO'] = [Fila1_dict, Fila2_dict, ...]
                    #Fila1_dict = {'CPEDIDO': val1, 'CCLIENTE': val2, 'FECHA_PEDIDO': val3} 
                out[t] = rows
            except pyodbc.Error as e: #Por si la tabla no existe
                if "ORA-00942" in str(e): # Si el error es especificamente que la tabla no existe, lista vacia y seguimos
                    out[t] = []
                else: # Si es otro error, peta
                    raise
        cur.close()
        return out #Devuelve el dict con todas las tablas y sus filas
    finally:
        if owns:
            cn_mgr.__exit__(None, None, None) #Cierra la conexion propia si la creó


# ----------------------------
# Gestión de transacciones
# ----------------------------
def begin_transaction() -> pyodbc.Connection:
    """Abre y devuelve una conexión con autocommit=False para trabajar en una transacción."""
    driver = _find_oracle_driver()
    return pyodbc.connect(_connect_string(driver), autocommit=False, timeout=5)


def commit_transaction(cn: pyodbc.Connection) -> None:
    cn.commit()


def rollback_transaction(cn: pyodbc.Connection) -> None:
    cn.rollback()


def savepoint(cn: pyodbc.Connection, name: str) -> None:
    cur = cn.cursor()
    cur.execute(f"SAVEPOINT {name}")
    cur.close()


# ----------------------------
# Operaciones del pedido
# ----------------------------
def insert_pedido(cn: pyodbc.Connection, cpedido: int, ccliente: int, fecha: date) -> None:
    cur = cn.cursor()
    cur.execute(
        "INSERT INTO PEDIDO (CPEDIDO, CCLIENTE, FECHA_PEDIDO) VALUES (?, ?, ?)",
        (cpedido, ccliente, fecha),
    )
    cur.close()


def _get_stock(cn: pyodbc.Connection, cproducto: int) -> int:
    cur = cn.cursor()
    cur.execute("SELECT CANTIDAD FROM STOCK WHERE CPRODUCTO = ?", (cproducto,))
    row = cur.fetchone()
    cur.close()
    if not row:
        raise ValueError(f"Producto {cproducto} no existe en STOCK")
    return int(row[0])


def insert_detalle(cn: pyodbc.Connection, cpedido: int, cproducto: int, cantidad: int) -> None:
    """Añade un detalle si hay stock suficiente; actualiza el stock (decrementa)."""
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser positiva")
    # Comprobar stock
    disponible = _get_stock(cn, cproducto)
    if disponible < cantidad:
        raise ValueError(f"Stock insuficiente: disponible={disponible}, pedido={cantidad}")
    # Insert detalle + actualizar stock
    cur = cn.cursor()
    cur.execute(
        "INSERT INTO DETALLE_PEDIDO (CPEDIDO, CPRODUCTO, CANTIDAD) VALUES (?, ?, ?)",
        (cpedido, cproducto, cantidad),
    )
    cur.execute(
        "UPDATE STOCK SET CANTIDAD = CANTIDAD - ? WHERE CPRODUCTO = ?",
        (cantidad, cproducto),
    )
    cur.close()


def delete_detalles_via_savepoint(cn: pyodbc.Connection, sp_name: str = "CAB") -> None:  # TODO RREFACTOR NAME
    """Elimina todos los detalles desde el savepoint de cabecera (revierten también los stocks)."""
    # Con Oracle basta con hacer rollback al savepoint creado tras la cabecera
    cur = cn.cursor()
    # Ambas formas son válidas, usamos la explícita por claridad:
    cur.execute(f"ROLLBACK TO SAVEPOINT {sp_name}")
    cur.close()


def cancel_pedido(cn: pyodbc.Connection) -> None:
    """Cancela todo lo hecho en la transacción actual (cabecera + detalles + stock)."""
    rollback_transaction(cn)


# (Opcional) utilidades para borrado total (fuera de la transacción de alta)   NO LO USAMOS (DEPRECATED)
def drop_all_user_tables() -> dict:
    with connect(autocommit=False) as cn:
        cur = cn.cursor()
        cur.execute("SELECT table_name FROM user_tables")
        names = [row[0] for row in cur.fetchall()]
        dropped = []
        for name in names:
            try:
                cur.execute(f'DROP TABLE "{name}" CASCADE CONSTRAINTS')
                dropped.append(name)
            except pyodbc.Error as e:
                if "ORA-00942" not in str(e):
                    raise
        cn.commit()
        cur.close()
        return {"dropped": dropped, "count": len(dropped)}
