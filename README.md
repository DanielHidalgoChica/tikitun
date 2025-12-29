# Practica 3: Tikitún
Para usar el entorno virtual de python con las
cosas que necesitamos los pasos son los siguientes:

0. Tener instalado Oracle Instant Client Basic y OCDB con todo lo que necesiten:
	0.1 Instalar paquetes con sudo: python3, pip, python3-venv, python3-tk, unixodbc, unixodbc-dev, odbcinst, libaio1t46, libnsl2
	0.2 En la página: https://www.oracle.com/es/database/technologies/releasenote-odbc-ic.html descargar los dos comprimidos en .zip correspondientes
	0.3 Los mueves a la carpeta `/opt/oracle` y descomprimes AMBOS AL MISMO NIVEL en un hijo
	0.4 Ejecutar con sudo script de `odbc_update_ini.sh` tirando como primer y único parámetro el directorio raíz `/`
	0.5 Haces ./run_app.sh y debería aparecer como "not found" solo la libaio.so.1
		Si te falta alguna otra, duro, llama al teléfono de asistencia al cliente de Oracle

	0.5.1 Para arreglarlo, `ln -sl /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /opt/oracle/instant_clinent_23_26/libaio.so.1`


1. Tener instalados python3, pip y python3-venv (módulo para crear
entornos virtuales)

2. Para activar el entorno virtual, creamos `python3 -m venv .venv` y lo activamos `source .venv/bin/activate`

3. Para instalar las dependencias dentro del entorno `pip install -r requirements.txt`

4. Para salir del entorno `deactivate`

También deberemos tener un archivo .env cada uno, que será privado, en el que
guardaremos nuestras credenciales de las bases de datos, y que luego podremos
cargar en python con `load_dotenv`. Será de la forma:

(archivo .env)
ORACLE_HOST=oracle0.ugr.es
ORACLE_PORT=1521
ORACLE_SERVICE=practbd
ORACLE_USER=x00000000
ORACLE_PASSWORD=tu_clave
