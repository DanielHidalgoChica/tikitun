import tkinter as tk
from tkinter import messagebox
from src.db.db_app import begin_transaction, commit, rollback
from src.services.productos_service import buscar_productos

def open_buscar_productos(parent):
    win = tk.Toplevel(parent)
    win.title("Buscar productos (stub)")
    win.geometry("520x320")

    tk.Label(win, text="Texto de búsqueda").pack()
    e_q = tk.Entry(win, width=50)
    e_q.pack(pady=6)

    out = tk.Text(win, width=62, height=12)
    out.pack(pady=8)

    def on_buscar():
        out.delete("1.0", tk.END)
        cn = begin_transaction()
        try:
            rows = buscar_productos(cn, {"q": e_q.get().strip()})
            commit(cn)
            for r in rows:
                out.insert(tk.END, f"- #{r['id_producto']} {r['titulo']} | {r['precio']}€ | {r['vendedor']}\n")
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", str(ex))

    tk.Button(win, text="Buscar", command=on_buscar).pack()
