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

# --- Configuración de encoding para Oracle (UTF-8) ---
# Esto asegura que los caracteres especiales (tildes, ñ, etc.) se manejen correctamente
os.environ["NLS_LANG"] = ".AL32UTF8"

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


def initialize_database(
    sql_dir: Optional[str] = None,
    files: Optional[List[str]] = None,
    drop_first: bool = True,
) -> dict:
    """Inicializa la base de datos ejecutando una lista de scripts SQL.

    Args:
        sql_dir: Carpeta donde buscar los ficheros SQL. Si es None, se usa el directorio `src/db` del paquete.
        files: Lista de nombres de fichero SQL a ejecutar en orden. Por defecto ['init.sql'].
        drop_first: Si es True (por defecto), primero hace DROP TABLE de todas las tablas
            del esquema respetando el orden de dependencias (FK) para evitar errores.

    Returns:
        Dict con resumen: {'executed_files': [...], 'statements_executed': n, 'dropped_tables': [...]}

    Raises:
        FileNotFoundError: si falta algún fichero SQL.
        Exception: si la ejecución SQL falla (se hace rollback y se propaga la excepción).
    """
    if files is None:
        files = ["init.sql"]

    # Determinar directorio por defecto (carpeta donde está este archivo -> src/db)
    if sql_dir is None:
        sql_dir = str(Path(__file__).resolve().parent)

    executed = []
    stmt_count = 0
    skipped_count = 0
    skipped_details = []
    dropped_tables: List[str] = []

    with connect(autocommit=False) as cn:
        cur = cn.cursor()
        try:
            # --- DROP TABLES FIRST ---
            if drop_first:
                # Obtener todas las tablas del usuario en orden de dependencias (hijos primero)
                # Usamos una consulta que ordena por profundidad de FK
                cur.execute("""
                    SELECT table_name FROM (
                        SELECT table_name, LEVEL AS lvl
                        FROM (
                            SELECT uc.table_name, ucc.table_name AS parent
                            FROM user_constraints uc
                            LEFT JOIN user_constraints ucc
                              ON uc.r_constraint_name = ucc.constraint_name
                             AND ucc.constraint_type = 'P'
                            WHERE uc.constraint_type = 'R'
                            UNION ALL
                            SELECT table_name, NULL FROM user_tables
                        )
                        START WITH parent IS NULL
                        CONNECT BY PRIOR table_name = parent
                    )
                    GROUP BY table_name
                    ORDER BY MAX(lvl) DESC
                """)
                tables_to_drop = [row[0] for row in cur.fetchall()]

                for tbl in tables_to_drop:
                    try:
                        cur.execute(f'DROP TABLE "{tbl}" CASCADE CONSTRAINTS PURGE')
                        dropped_tables.append(tbl)
                    except pyodbc.Error as e:
                        err = str(e)
                        # ORA-00942: table or view does not exist (ignorar)
                        if 'ORA-00942' not in err:
                            raise

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
                                skipped_count += 1
                                skipped_details.append(f"CREATE TABLE {table_name}")
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
                            skipped_count += 1
                            detail = s.splitlines()[0]
                            skipped_details.append(detail)
                            executed.append(f"skipped (already exists): {detail}")
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

    return {
        "executed_files": executed,
        "statements_executed": stmt_count,
        "skipped_statements": skipped_count,
        "skipped_details": skipped_details,
        "dropped_tables": dropped_tables,
    }
