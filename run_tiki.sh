#!/usr/bin/env bash
export IC_HOME=/opt/oracle/instantclient_23_26
export LD_LIBRARY_PATH="$IC_HOME:/usr/lib/x86_64-linux-gnu"
ldd /opt/oracle/instantclient_23_26/libsqora.so.23.1
source .venv/bin/activate
pip install -r requirements.txt > /dev/null
#exec streamlit run app.py
exec python -m src.app
