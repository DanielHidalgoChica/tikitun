"""
Ventana para confirmar ventas y puntuar productos
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.ventas.ventas_service import confirmar_recepcion, puntuar_venta, obtener_ventas_como_comprador
from src.services.productos.consulta_service import consultar_producto


def open_confirmar_venta(parent, id_producto: int, username: str):

    win = tk.Toplevel(parent)
    win.title(f"Confirmar y puntuar venta - Producto {id_producto}")
    win.geometry("540x360")
    win.resizable(False, False)

    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    ventas = None

    try:
        with connect() as cn:
            prod = consultar_producto(cn, id_producto)
            ventas = obtener_ventas_como_comprador(cn, username)
    except Exception as e:
        messagebox.showerror("Error", str(e), parent=win)
        win.destroy()
        return

    venta = next((v for v in ventas if v["id_producto"] == id_producto), None)

    if not venta:
        messagebox.showerror(
            "Error",
            "Este producto no está registrado como compra tuya.",
            parent=win
        )
        win.destroy()
        return

    confirmada = venta["recepcion_confirmada"]
    valoracion = venta["valoracion"]

    tk.Label(frame, text="Confirmar recepción y puntuar",
             font=("Arial", 13, "bold")).pack(pady=(0, 15))

    tk.Label(frame, text=f"Producto: {prod['titulo']}").pack(anchor="w")
    tk.Label(frame, text=f"Precio final: {venta['precio_final']} €")\
        .pack(anchor="w", pady=(0, 15))

    estado = "CONFIRMADA" if confirmada else "PENDIENTE"
    tk.Label(frame, text=f"Estado: {estado}",
             fg="green" if confirmada else "orange",
             font=("Arial", 10, "bold"))\
        .pack(anchor="w", pady=(0, 10))

    if confirmada:
        tk.Label(frame,
                 text=f"Valoración: {valoracion}/5",
                 font=("Arial", 10, "bold"))\
            .pack(anchor="w")

        tk.Button(frame, text="Cerrar",
                  command=win.destroy,
                  width=15)\
            .pack(pady=20)
        return

    tk.Label(frame, text="Puntuación (0 - 5)",
             font=("Arial", 10, "bold"))\
        .pack(anchor="w")

    e_puntuacion = tk.Entry(frame, width=10)
    e_puntuacion.pack(anchor="w", pady=(5, 15))
    e_puntuacion.focus()

    def confirmar_y_puntuar():
        val = e_puntuacion.get().strip()

        try:
            puntuacion = float(val)
            if not (0 <= puntuacion <= 5):
                raise ValueError

            cn = begin_transaction()
            try:
                confirmar_recepcion(cn, id_producto, username)
                puntuar_venta(cn, id_producto, puntuacion)
                commit(cn)

                messagebox.showinfo(
                    "Correcto",
                    "Recepción confirmada y puntuación registrada.",
                    parent=win
                )
                win.destroy()

            except Exception as ex:
                rollback(cn)
                messagebox.showerror("Error", str(ex), parent=win)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Introduce una puntuación válida entre 0 y 5, con saltos de 0.5",
                parent=win
            )

    btns = tk.Frame(frame)
    btns.pack(pady=10)

    tk.Button(btns,
              text="Confirmar y puntuar",
              command=confirmar_y_puntuar,
              bg="#4CAF50",
              fg="white",
              width=18)\
        .pack(side=tk.LEFT, padx=5)

    tk.Button(btns,
              text="Cancelar",
              command=win.destroy,
              width=18)\
        .pack(side=tk.LEFT, padx=5)
