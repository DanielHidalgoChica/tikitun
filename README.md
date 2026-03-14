# <img width="43" height="43" alt="logo" src="https://github.com/user-attachments/assets/04d602e4-f292-4850-bd7b-3204df87fb36" /> TikiTún 


Desktop application for **peer-to-peer product buying and selling**, developed as a practical assignment for the **Information Systems Design and Development** course at the University of Granada.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Oracle](https://img.shields.io/badge/Database-Oracle-red?logo=oracle)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/license-AGPL--v3-blue)

---

## 📋 Description

TikiTún is a multi-user information system that manages the complete lifecycle of a transaction: product listing, search with personalized recommendations, user negotiation, and sale confirmation with reviews.

---

## ✨ Key Features

### 📍 Recommendation System
The feed filters products based on the **distance between buyer and seller**, calculating if the sum of their availability ranges covers the geographical distance between them. Products are sorted by:
1. Match with the user's preferred categories
2. Promotion level (decays by 0.1 per day)
3. Number of users who have favorited the product

### 🤝 Counteroffer System
Buyers can propose alternative prices. The seller views all received offers and can accept or reject each one, automating the fund transfer upon acceptance.

### 🚀 Product Promotion
Sellers can pay to increase the visibility of their products. The cost is proportional to the item's price, and the promotion level **decays linearly** over time.

### 🔥 Data Integrity Triggers
The database implements **PL/SQL triggers** that ensure consistency:
* Automatic update of the favorites counter
* Archiving of conversations upon completed sales
* Data cleanup upon account deletion
* And many more features

---

## 🏗️ Architecture

The project follows a **layered architecture** with a clear separation of concerns:

```text
src/
├── app.py                  # Entry point
├── db/                     # ODBC Connection and SQL scripts
│   ├── init.sql            # DDL + Triggers
│   └── seed_test_data.sql  # Test data
├── repositories/           # Repository Pattern (data access)
│   ├── perfiles/
│   ├── productos/
│   ├── mensajes/
│   ├── ventas/
│   └── feed_busqueda_favs/
├── services/               # Business logic
└── ui/                     # Tkinter Interface
```

### Subsystems

| Module | Description |
|--------|-------------|
| 👤 **Profiles** | Registration, authentication, preferences, and wallet |
| 📦 **Products** | Item CRUD, images, and promotions |
| 🔍 **Feed & Search** | Recommendations, filtered search, and favorites |
| 💳 **Sales** | Purchases, counteroffers, and reviews |
| 💬 **Messaging** | Product-linked chat |

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.10+ |
| Database | Oracle |
| DB Connection | pyodbc |
| Interface | Tkinter |

---

## 🚀 Installation

### 0. Configure Oracle Instant Client (Instructions for Linux Ubuntu 24.04)

> ⚠️ Only required the first time on the system

1. **Install system dependencies:**
```bash
sudo apt install python3 python3-pip python3-venv python3-tk unixodbc unixodbc-dev odbcinst libaio1t64 libnsl2
```

2. **Download Oracle Instant Client:**
   - Go to [Oracle ODBC Downloads](https://www.oracle.com/es/database/technologies/releasenote-odbc-ic.html)
   - Download **Basic** and **ODBC** (both `.zip`)

3. **Install in `/opt/oracle`:**
```bash
sudo mkdir -p /opt/oracle
sudo mv instantclient-*.zip /opt/oracle/
cd /opt/oracle
sudo unzip instantclient-basic-*.zip
sudo unzip instantclient-odbc-*.zip   # Unzip at the same level
```

4. **Configure ODBC:**
```bash
sudo /opt/oracle/instantclient_23_26/odbc_update_ini.sh /
```

5. **Fix for `libaio.so.1`** (if it appears as "not found"):
```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /opt/oracle/instantclient_23_26/libaio.so.1
```

### 1. Clone and install

```bash
git clone [https://github.com/your-username/tikitun.git](https://github.com/your-username/tikitun.git)
cd tikitun
```

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
ORACLE_HOST=oracle0.ugr.es
ORACLE_PORT=1521
ORACLE_SERVICE=practbd
ORACLE_USER=x00000000
ORACLE_PASSWORD=your_password
```

### 3. Initialize the database

Execute in your Oracle SQL client:
```sql
-- 1. Create tables and triggers
@src/db/init.sql

-- 2. (Optional) Load test data
@src/db/seed_test_data.sql
```

### 4. Run

```bash
./run_tiki.sh
```

> The script automatically configures the Oracle environment variables, activates the virtual environment, and installs dependencies if necessary.

---

## 👥 Authors

| Name | Subsystem |
|--------|------------|
| Aitor de la Iglesia García | Messaging |
| Daniel Hidalgo Chica | Feed, Search & Favorites |
| Elsa Rodríguez Macmichael | Profile Management |
| Juan Manuel Fernández García | Sales Management |
| Roberto González Lugo | Product Management |

---

**University of Granada** — DDSI, Academic Year 2024/2025
