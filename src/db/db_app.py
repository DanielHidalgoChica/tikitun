# ------------------------------------------------------------
# db_app.py  —  Capa de acceso a datos para TikiTun
# Basado en el código del seminario (OLD/db_app.py)
# ------------------------------------------------------------
import os
import pyodbc
from contextlib import contextmanager
from typing import Optional
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
    """Genera la cadena de conexión ODBC a Oracle."""
    return (
        f"DRIVER={{{driver}}};"
        f"DBQ=//{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE};"
        f"UID={ORACLE_USER};PWD={ORACLE_PASSWORD};"
    )


@contextmanager
def connect(autocommit: bool = False):
    """Abre una conexión ODBC a Oracle (por defecto autocommit=False).
    Se usa con 'with' para garantizar cierre automático.
    
    Ejemplo:
        with connect() as cn:
            cur = cn.cursor()
            cur.execute("SELECT * FROM USUARIOS")
    """
    driver = _find_oracle_driver()
    cn = pyodbc.connect(_connect_string(driver), autocommit=autocommit, timeout=5)
    try:
        yield cn
    finally:
        cn.close()


# ----------------------------
# Gestión de transacciones
# ----------------------------
def begin_transaction() -> pyodbc.Connection:
    """Abre y devuelve una conexión con autocommit=False para trabajar en una transacción.
    
    Ejemplo:
        cn = begin_transaction()
        try:
            # ... operaciones ...
            commit(cn)
        except Exception:
            rollback(cn)
    """
    driver = _find_oracle_driver()
    return pyodbc.connect(_connect_string(driver), autocommit=False, timeout=5)


def commit(cn: pyodbc.Connection) -> None:
    """Confirma (COMMIT) la transacción actual."""
    cn.commit()


def rollback(cn: pyodbc.Connection) -> None:
    """Revierte (ROLLBACK) la transacción actual."""
    cn.rollback()


def savepoint(cn: pyodbc.Connection, name: str) -> None:
    """Crea un SAVEPOINT con el nombre especificado."""
    cur = cn.cursor()
    cur.execute(f"SAVEPOINT {name}")
    cur.close()


def rollback_to_savepoint(cn: pyodbc.Connection, name: str) -> None:
    """Revierte hasta un SAVEPOINT específico."""
    cur = cn.cursor()
    cur.execute(f"ROLLBACK TO SAVEPOINT {name}")
    cur.close()
