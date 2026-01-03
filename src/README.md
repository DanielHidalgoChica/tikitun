Aquí tienes un **README sólido, claro y defendible** para la práctica de **TikiTun**, explicando **el esquema, el porqué y cómo se usa**, pensado para DDSI y para que cualquiera del grupo lo entienda aunque no sepa desarrollo.

Puedes copiarlo tal cual a `README.md`.

---

# TikiTun – Esqueleto de Aplicación (Práctica DDSI)

## 1. Descripción general

**TikiTun** es una aplicación tipo *Wallapop* desarrollada como parte de las prácticas de **DDSI**.
Este repositorio contiene un **esqueleto completamente funcional** de la aplicación:

* Se puede ejecutar.
* Tiene interfaz gráfica (Tkinter).
* Implementa el **workflow completo**:
  **Interfaz → Lógica → Acceso a datos → Transacciones**.
* **NO** implementa todavía la lógica real ni el SQL definitivo.

El objetivo es disponer de una base clara y estable sobre la que desarrollar las funcionalidades finales definidas en las prácticas anteriores (RF/RS, DFD, modelo relacional).

---

## 2. Objetivo de este esqueleto

Este proyecto sirve para:

* Tener **la arquitectura definitiva** desde el primer momento.
* Permitir al grupo:

  * repartir tareas sin pisarse,
  * desarrollar funcionalidades de forma incremental,
  * cumplir con los criterios de separación por capas exigidos en DDSI.
* Poder explicar fácilmente el sistema al profesor.

Nada de este esquema se rehace más adelante: **solo se rellena**.

---

## 3. Arquitectura general

La aplicación sigue una **arquitectura por capas**:

```
Interfaz (UI)
   ↓
Servicios (Lógica de negocio / RS)
   ↓
Repositorios (SQL / Acceso a BD)
   ↓
Base de datos + Transacciones
```

Cada capa tiene **una responsabilidad clara** y no invade a las demás.

---

## 4. Estructura de carpetas

```
tikitun/
├── src/
│   ├── app.py                  # Punto de entrada de la aplicación
│   │
│   ├── db/                     # Gestión de BD y transacciones
│   │   ├── db_app.py
│   │   └── __init__.py
│   │
│   ├── repositories/           # Acceso a datos (SQL)
│   │   ├── productos_repo.py
│   │   ├── chats_repo.py
│   │   ├── mensajes_repo.py
│   │   ├── usuarios_repo.py
│   │   └── __init__.py
│   │
│   ├── services/               # Lógica de negocio (RS)
│   │   ├── productos_service.py
│   │   ├── chats_service.py
│   │   ├── mensajes_service.py
│   │   ├── usuarios_service.py
│   │   └── __init__.py
│   │
│   └── ui/                     # Interfaz gráfica (Tkinter)
│       ├── main_window.py
│       ├── publicar_producto_window.py
│       ├── buscar_productos_window.py
│       ├── abrir_chat_window.py
│       ├── enviar_mensaje_window.py
│       └── __init__.py
│
└── OLD/                        # Código del seminario 1 (referencia)
```

---

## 5. Explicación de cada capa

### 5.1 UI (Interfaz de usuario)

📁 `src/ui/`

Contiene **las ventanas Tkinter**.

Responsabilidades:

* Mostrar pantallas.
* Recoger datos del usuario.
* Mostrar mensajes de error o éxito.
* Llamar a los *services*.

❌ NO hace:

* SQL
* validaciones complejas
* commits ni rollbacks

Ejemplos:

* Publicar producto
* Buscar productos
* Abrir chat
* Enviar mensaje

---

### 5.2 Services (Lógica de negocio)

📁 `src/services/`

Aquí vive la **lógica del sistema**:

* reglas de negocio (RS),
* comprobaciones,
* coordinación de operaciones.

Responsabilidades:

* Validar datos.
* Decidir si una acción está permitida.
* Llamar a uno o varios repositories.
* Usar *savepoints* si es necesario.

❌ NO hace:

* interfaces gráficas
* SQL directo
* commit / rollback

Ejemplo:

> “Para abrir un chat, el comprador y vendedor deben ser distintos y existir.”

---

### 5.3 Repositories (Acceso a datos)

📁 `src/repositories/`

Aquí está el **SQL puro** (actualmente simulado).

Responsabilidades:

* `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
* Traducir datos entre BD y Python.

❌ NO hace:

* reglas de negocio
* validaciones funcionales
* decisiones

Cada repository suele corresponderse con una **tabla final** del modelo (tras la fusión de almacenes).

---

### 5.4 db_app (Base de datos y transacciones)

📁 `src/db/db_app.py`

Controla las **transacciones**.

Actualmente:

* usa una conexión *fake* (prints por consola).

Más adelante:

* se sustituirá por Oracle (`pyodbc`) usando la BD de la universidad.

Funciones clave:

* `begin_transaction()`
* `commit()`
* `rollback()`
* `savepoint()`

⚠️ **Solo aquí se hace commit/rollback**.

---

## 6. Flujo de ejecución (ejemplo real)

**Caso de uso: Publicar producto**

1. Usuario pulsa “Guardar” (UI).
2. Se abre una transacción.
3. UI llama a `productos_service.publicar_producto()`.
4. El service:

   * valida datos,
   * crea un savepoint,
   * llama al repository.
5. El repository “inserta” el producto.
6. Todo OK → commit.
7. Error → rollback.
8. UI muestra mensaje.

Este flujo ya está implementado, aunque sea con datos simulados.

---

## 7. Ejecución del proyecto

Desde la carpeta raíz (`tikitun/`):

```bash
python -m src.app
```

⚠️ No ejecutar archivos sueltos (`python app.py`), siempre como módulo.

---

## 8. Estado actual del proyecto

✔ Arquitectura final definida
✔ App ejecutable
✔ Navegación completa
✔ Flujo de transacciones visible por consola

❌ SQL real (pendiente)
❌ Reglas completas (pendiente)
❌ Conexión Oracle real (pendiente)

---

## 9. Próximos pasos

1. Sustituir `db_app.py` por conexión real a Oracle.
2. Implementar SQL real en `repositories`.
3. Implementar RS reales en `services`.
4. Mejorar UI (listados reales, estados, etc.).

Todo esto se hace **sin cambiar la estructura**.

---

## 10. Regla de oro del proyecto

* UI **no sabe SQL**
* Repository **no sabe reglas**
* Service **no pinta pantallas**
* DB **controla transacciones**

Si se cumple esto, la práctica está bien planteada.

---
