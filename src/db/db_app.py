# ------------------------------------------------------------
# db_app.py  —  Capa de acceso a datos para TikiTun
# Basado en el código del seminario (OLD/db_app.py)
# ------------------------------------------------------------
import os
import pyodbc
from contextlib import contextmanager
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path
from typing import List
import re

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


def initialize_database(sql_dir: Optional[str] = None, files: Optional[List[str]] = None) -> dict:
    """Inicializa la base de datos ejecutando una lista de scripts SQL.

    Args:
        sql_dir: Carpeta donde buscar los ficheros SQL. Si es None, se usa el directorio `src/db` del paquete.
        files: Lista de nombres de fichero SQL a ejecutar en orden. Por defecto
            ['init.sql', 'insert_test_tuples.sql'].

    Returns:
        Dict con resumen: {'executed_files': [...], 'statements_executed': n}

    Raises:
        FileNotFoundError: si falta algún fichero SQL.
        Exception: si la ejecución SQL falla (se hace rollback y se propaga la excepción).
    """
    if files is None:
        files = ["init.sql", "insert_test_tuples.sql"]

    # Determinar directorio por defecto (carpeta donde está este archivo -> src/db)
    if sql_dir is None:
        sql_dir = str(Path(__file__).resolve().parent)

    executed = []
    stmt_count = 0

    with connect(autocommit=False) as cn:
        cur = cn.cursor()
        try:
            for fname in files:
                path = Path(sql_dir) / fname
                if not path.exists():
                    raise FileNotFoundError(f"SQL file not found: {path}")

                sql_text = path.read_text(encoding="utf-8")

                # Intenta dividir por ';' para obtener sentencias independientes.
                # Se eliminan líneas vacías resultantes.
                statements = [s.strip() for s in sql_text.split(";") if s.strip()]

                for stmt in statements:
                    s = stmt.strip()
                    if not s:
                        continue

                    # Si la sentencia es CREATE TABLE y la tabla ya existe, la saltamos
                    if re.match(r'(?i)^create\s+table', s):
                        m = re.search(r'(?i)^create\s+table\s+"?([A-Za-z0-9_$]+)"?', s)
                        table_name = m.group(1) if m else None
                        if table_name:
                            exists = 0
                            try:
                                cur.execute("SELECT COUNT(*) FROM user_tables WHERE table_name = ?", (table_name.upper(),))
                                row = cur.fetchone()
                                exists = row[0] if row else 0
                            except Exception:
                                # Si la consulta de existencia falla, no asumimos que exista
                                exists = 0

                            if exists and exists > 0:
                                executed.append(f"skipped CREATE TABLE {table_name}")
                                continue

                    # Ejecutar la sentencia y capturar errores de "objeto ya existe"
                    try:
                        cur.execute(s)
                        stmt_count += 1
                    except pyodbc.Error as e:
                        err = str(e)
                        # ORA-00955: name is already used by an existing object
                        if 'ORA-00955' in err or 'already exists' in err.lower() or 'name is already used' in err.lower():
                            executed.append(f"skipped (already exists): {s.splitlines()[0]}")
                            continue
                        # Propagar otros errores
                        raise

                executed.append(str(path))

            # Confirmar todos los cambios si todo fue bien
            cn.commit()
        except Exception:
            # Si hay error, revertir y propagar
            try:
                cn.rollback()
            except Exception:
                pass
            raise
        finally:
            cur.close()

    return {"executed_files": executed, "statements_executed": stmt_count}
