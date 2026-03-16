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
## Usage examples

**User creation, login and posting of a product**

<div style="text-align: center; width: 100%;">
  <img src="https://github.com/user-attachments/assets/76dd2813-2813-41a9-b957-cf782064c05c" alt="login_post_prod_ULTRA" style="width: 100%; max-width: 100%; height: auto; display: block; margin: 0 auto;">
</div>



---


## 🏗️ Architecture

The project follows a **layered architecture** with a clear separation of concerns:

```text
src/
├── app.py                  # Entry point
├── db/                     # ODBC connection + Oracle SQL scripts
│   ├── init.sql            # DDL + Triggers
│   ├── drop_all.sql        # Drop previous objects
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
| DB Connection | pyodbc + sqlplus (schema initialization) |
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
   - Go to [Oracle ODBC Downloads](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html)
   - Download **Basic**, **ODBC** and **SQL*Plus** (all of them on `.zip`)

3. **Install in `/opt/oracle`:**
```bash
sudo mkdir -p /opt/oracle
sudo mv instantclient-*.zip /opt/oracle/
cd /opt/oracle
sudo unzip instantclient-basic-*.zip
sudo unzip instantclient-odbc-*.zip   
sudo unzip instantclient-sqlplus-*.zip # Unzip at the same level
```

4. **Configure ODBC:**
```bash
sudo /opt/oracle/instantclient_23_26/odbc_update_ini.sh /
```

5. **Fix for `libaio.so.1`** (if it appears as "not found" when running `run_tiki.sh`):
```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /opt/oracle/instantclient_23_26/libaio.so.1
```

### 1. Clone

```bash
git clone https://github.com/DanielHidalgoChica/tikitun.git
cd tikitun
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

### 3. Run (with or without DB initialization)

Normal startup:
```bash
./run_tiki.sh
```

Initialize database + launch app (single command):
```bash
./run_tiki.sh --init-db
./run_tiki.sh --init-db --with-seed
```
It's necessary to be connected to the UGR's VPN for the database connection to work.

> `run_tiki.sh` now handles the full flow: environment setup, dependency install, optional Oracle schema initialization through `sqlplus`, and app startup.

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
