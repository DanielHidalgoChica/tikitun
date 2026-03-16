#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

dotenv_get() {
    local key="$1"
    local env_file="$2"
    local line value

    line=$(grep -m1 -E "^${key}=" "$env_file" 2>/dev/null || true)
    value="${line#*=}"

    # Quitar comillas simples/dobles de borde si existen
    value="${value#\"}"
    value="${value%\"}"
    value="${value#\'}"
    value="${value%\'}"

    printf '%s' "$value"
}

# Configurar Oracle Instant Client
export IC_HOME=/opt/oracle/instantclient_23_26
export LD_LIBRARY_PATH="$IC_HOME:$LD_LIBRARY_PATH"

# Check if the virtual environment exists; if not, create it
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activar entorno virtual e instalar dependencias
source .venv/bin/activate
pip install -r requirements.txt

# Inicializar BD opcionalmente
# Uso: ./run_tiki.sh --init-db [--with-seed]
if [[ "$1" == "--init-db" ]]; then
    SQLPLUS_BIN=""
    if command -v sqlplus >/dev/null 2>&1; then
        SQLPLUS_BIN="$(command -v sqlplus)"
    elif [[ -x "$IC_HOME/sqlplus" ]]; then
        SQLPLUS_BIN="$IC_HOME/sqlplus"
    else
        echo "❌ sqlplus no está disponible en PATH ni en $IC_HOME/sqlplus"
        exit 1
    fi

    ENV_ORACLE_HOST=""
    ENV_ORACLE_PORT=""
    ENV_ORACLE_SERVICE=""
    ENV_ORACLE_USER=""
    ENV_ORACLE_PASSWORD=""

    if [[ -f "$SCRIPT_DIR/.env" ]]; then
        ENV_ORACLE_HOST="$(dotenv_get "ORACLE_HOST" "$SCRIPT_DIR/.env")"
        ENV_ORACLE_PORT="$(dotenv_get "ORACLE_PORT" "$SCRIPT_DIR/.env")"
        ENV_ORACLE_SERVICE="$(dotenv_get "ORACLE_SERVICE" "$SCRIPT_DIR/.env")"
        ENV_ORACLE_USER="$(dotenv_get "ORACLE_USER" "$SCRIPT_DIR/.env")"
        ENV_ORACLE_PASSWORD="$(dotenv_get "ORACLE_PASSWORD" "$SCRIPT_DIR/.env")"
    fi

    ORACLE_HOST="${ORACLE_HOST:-${ENV_ORACLE_HOST:-oracle0.ugr.es}}"
    ORACLE_PORT="${ORACLE_PORT:-${ENV_ORACLE_PORT:-1521}}"
    ORACLE_SERVICE="${ORACLE_SERVICE:-${ENV_ORACLE_SERVICE:-practbd}}"
    ORACLE_USER="${ORACLE_USER:-$ENV_ORACLE_USER}"
    ORACLE_PASSWORD="${ORACLE_PASSWORD:-$ENV_ORACLE_PASSWORD}"

    if [[ -z "${ORACLE_USER:-}" || -z "${ORACLE_PASSWORD:-}" ]]; then
        echo "❌ Faltan ORACLE_USER/ORACLE_PASSWORD en .env"
        exit 1
    fi

    CONN_STR="${ORACLE_USER}/${ORACLE_PASSWORD}@//${ORACLE_HOST}:${ORACLE_PORT}/${ORACLE_SERVICE}"

    echo "🚀 Inicializando base de datos con sqlplus..."

    if [[ "$2" == "--with-seed" ]]; then
        "$SQLPLUS_BIN" -L "$CONN_STR" <<SQL
WHENEVER SQLERROR EXIT SQL.SQLCODE
SET DEFINE OFF
@${SCRIPT_DIR}/src/db/drop_all.sql
/
@${SCRIPT_DIR}/src/db/init.sql
@${SCRIPT_DIR}/src/db/seed_test_data.sql
EXIT
SQL
    else
        "$SQLPLUS_BIN" -L "$CONN_STR" <<SQL
WHENEVER SQLERROR EXIT SQL.SQLCODE
SET DEFINE OFF
@${SCRIPT_DIR}/src/db/drop_all.sql
/
@${SCRIPT_DIR}/src/db/init.sql
EXIT
SQL
    fi

    echo "✅ Inicialización completada"
fi

# Ejecutar aplicación
exec python3 -m src.app
