# 🛒 TikiTún

Aplicación de escritorio para **compraventa de productos entre particulares**, desarrollada como práctica de la asignatura **Diseño y Desarrollo de Sistemas de Información** en la Universidad de Granada.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Oracle](https://img.shields.io/badge/Database-Oracle-red?logo=oracle)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)

---

## 📋 Descripción

TikiTún es un sistema de información multiusuario que gestiona el ciclo completo de una transacción: publicación de productos, búsqueda con recomendaciones personalizadas, negociación entre usuarios, y confirmación de venta con valoraciones.

---

## ✨ Funcionalidades Destacadas

### 📍 Sistema de Recomendaciones
El feed filtra productos según la **distancia entre comprador y vendedor**, calculando si la suma de sus rangos de disponibilidad cubre la distancia geográfica entre ambos. Los productos se ordenan por:
1. Coincidencia con categorías preferidas del usuario
2. Grado de promoción (decae 0.1 por día)
3. Número de usuarios que tenga ese producto en "favoritos"

### 🤝 Sistema de Contraofertas
Los compradores pueden proponer precios alternativos. El vendedor visualiza todas las ofertas recibidas y puede aceptar o rechazar cada una, automatizando la transferencia de fondos si acepta.

### 🚀 Promoción de Productos
Los vendedores pueden pagar para aumentar la visibilidad de sus productos. El coste es proporcional al precio del artículo y el grado de promoción **decae linealmente** con el tiempo.

### 🔥 Triggers para Integridad de Datos
La base de datos implementa **disparadores PL/SQL** que garantizan la consistencia:
- Actualización automática del contador de favoritos
- Archivado de conversaciones al completar ventas
- Limpieza de datos al eliminar cuentas


---

## 🏗️ Arquitectura

El proyecto sigue una **arquitectura en capas** con separación clara de responsabilidades:

```
src/
├── app.py                  # Punto de entrada
├── db/                     # Conexión ODBC y scripts SQL
│   ├── init.sql            # DDL + Triggers
│   └── seed_test_data.sql  # Datos de prueba
├── repositories/           # Patrón Repository (acceso a datos)
│   ├── perfiles/
│   ├── productos/
│   ├── mensajes/
│   ├── ventas/
│   └── feed_busqueda_favs/
├── services/               # Lógica de negocio
└── ui/                     # Interfaz Tkinter
```

### Subsistemas

| Módulo | Descripción |
|--------|-------------|
| 👤 **Perfiles** | Registro, autenticación, preferencias y monedero |
| 📦 **Productos** | CRUD de artículos, imágenes y promociones |
| 🔍 **Feed y Búsqueda** | Recomendaciones, búsqueda filtrada y favoritos |
| 💳 **Ventas** | Compras, contraofertas y valoraciones |
| 💬 **Mensajería** | Chat vinculado a productos |

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.10+ |
| Base de Datos | Oracle |
| Conexión BD | pyodbc |
| Interfaz | Tkinter |

---

## 🚀 Instalación

### 0. Configurar Oracle Instant Client (Linux)

> ⚠️ Solo necesario la primera vez en el sistema

1. **Instalar dependencias del sistema:**
```bash
sudo apt install python3 python3-pip python3-venv python3-tk unixodbc unixodbc-dev odbcinst libaio1t64 libnsl2
```

2. **Descargar Oracle Instant Client:**
   - Ir a [Oracle ODBC Downloads](https://www.oracle.com/es/database/technologies/releasenote-odbc-ic.html)
   - Descargar **Basic** y **ODBC** (ambos `.zip`)

3. **Instalar en `/opt/oracle`:**
```bash
sudo mkdir -p /opt/oracle
sudo mv instantclient-*.zip /opt/oracle/
cd /opt/oracle
sudo unzip instantclient-basic-*.zip
sudo unzip instantclient-odbc-*.zip   # Descomprimir en el mismo nivel
```

4. **Configurar ODBC:**
```bash
sudo /opt/oracle/instantclient_23_26/odbc_update_ini.sh /
```

5. **Fix para `libaio.so.1`** (si aparece como "not found"):
```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /opt/oracle/instantclient_23_26/libaio.so.1
```


### 1. Clonar e instalar

```bash
git clone https://github.com/tu-usuario/tikitun.git
cd tikitun
```

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar credenciales

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:
```env
ORACLE_HOST=oracle0.ugr.es
ORACLE_PORT=1521
ORACLE_SERVICE=practbd
ORACLE_USER=x00000000
ORACLE_PASSWORD=tu_clave
```

### 3. Inicializar base de datos

Ejecutar en tu cliente SQL de Oracle:
```sql
-- 1. Crear tablas y triggers
@src/db/init.sql

-- 2. (Opcional) Cargar datos de prueba
@src/db/seed_test_data.sql
```

### 4. Ejecutar

```bash
./run_tiki.sh
```

> El script configura automáticamente las variables de entorno de Oracle, activa el entorno virtual e instala dependencias si es necesario.

---

## 👥 Autores

| Nombre | Subsistema |
|--------|------------|
| Aitor de la Iglesia García | Mensajería |
| Daniel Hidalgo Chica | Feed, Búsquedas y Favoritos |
| Elsa Rodríguez Macmichael | Gestión de Perfiles |
| Juan Manuel Fernández García | Gestión de Ventas |
| Roberto González Lugo | Gestión de Productos |

---

**Universidad de Granada** — DDSI, Curso 2024/2025
