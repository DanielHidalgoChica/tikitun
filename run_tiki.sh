#!/usr/bin/env bash

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
pip install -q -r requirements.txt

# Ejecutar aplicación
exec python3 -m src.app
