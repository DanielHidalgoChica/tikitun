"""Inicialización de base de datos sin SQL Developer/sqlplus.

Uso:
    python scripts/init_db.py
    python scripts/init_db.py --with-seed
    python scripts/init_db.py --no-drop
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Asegura que la raíz del proyecto (donde está `src/`) esté en el path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db.db_app import initialize_database


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inicializa el esquema Oracle de TikiTún usando pyodbc."
    )
    parser.add_argument(
        "--with-seed",
        action="store_true",
        help="También ejecuta src/db/seed_test_data.sql",
    )
    parser.add_argument(
        "--no-drop",
        action="store_true",
        help="No elimina tablas antes de crear/inicializar",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    files = ["init.sql"]
    if args.with_seed:
        files.append("seed_test_data.sql")

    try:
        print("🚀 Inicializando base de datos...")
        result = initialize_database(
            files=files,
            drop_first=not args.no_drop,
        )

        print("✅ Inicialización completada")
        print(f"   - Ficheros ejecutados: {len(result['executed_files'])}")
        print(f"   - Sentencias ejecutadas: {result['statements_executed']}")
        print(f"   - Sentencias omitidas: {result['skipped_statements']}")
        print(f"   - Tablas eliminadas: {len(result['dropped_tables'])}")

        if args.with_seed:
            print("🧪 Datos de prueba cargados")

        return 0

    except Exception as exc:
        print("❌ Error durante la inicialización de la base de datos")
        print(f"   {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
