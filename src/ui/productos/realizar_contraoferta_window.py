"""
Ventana para realizar una contraoferta.
"""

import tkinter as tk
from tkinter import messagebox
from src.db.db_app import begin_transaction, commit, rollback
from src.services.ventas.ventas_service import realizar_contraoferta

def open_realizar_contraoferta(id_producto: int, username: str):

    win = tk.Toplevel()
    win.title("Realizar contraoferta")
    win.geometry("420x240")
    win.resizable(False, False)

    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Formulario de contraoferta", font=("Arial", 12, "bold")).pack(pady=(0, 15))

    tk.Label(frame, text=f"Usuario: @{username}", font=("Arial", 10)).pack(anchor="w")
    tk.Label(frame, text=f"ID Producto: {id_producto}", font=("Arial", 10)).pack(anchor="w", pady=(0, 15))

    tk.Label(frame, text="Importe (€)", font=("Arial", 10, "bold")).pack(anchor="w")
    e_precio = tk.Entry(frame, width=20)
    e_precio.pack(anchor="w", pady=(5, 15))
    e_precio.focus()

    def enviar():
        valor = e_precio.get().strip()

        if not valor:
            messagebox.showwarning("Atención", "Introduce un importe")
            return

        try:
            precio = float(valor)
            if precio <= 0:
                raise ValueError
        
            cn = begin_transaction()
            try:
                realizar_contraoferta(cn, id_producto, username, precio)
                commit(cn)
                messagebox.showinfo("Correcto", "Contraoferta enviada correctamente")
                win.destroy()
            except Exception as ex:
                rollback(cn)
                messagebox.showerror("Error", str(ex))

        except ValueError:
            messagebox.showerror("Error", "Introduce un número válido mayor que 0")

    btns = tk.Frame(frame)
    btns.pack()

    tk.Button(btns, text="Enviar", command=enviar, bg="#2196F3", fg="white", width=14).pack(side=tk.LEFT, padx=5)
    tk.Button(btns, text="Cancelar", command=win.destroy, width=14).pack(side=tk.LEFT, padx=5)
