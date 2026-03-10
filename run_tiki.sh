#!/usr/bin/env bash

# Configurar Oracle Instant Client
export IC_HOME=/opt/oracle/instantclient_23_26
export LD_LIBRARY_PATH="$IC_HOME:$LD_LIBRARY_PATH"

# Activar entorno virtual e instalar dependencias
source .venv/bin/activate
pip install -q -r requirements.txt

# Ejecutar aplicación
exec python -m src.app
