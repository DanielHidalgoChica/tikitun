import tkinter as tk
from tkinter import messagebox
from src.db.db_app import begin_transaction, commit, rollback
from src.services.productos.productos_service import publicar_producto

def open_publicar_producto(parent):
    win = tk.Toplevel(parent)
    win.title("Publicar producto (stub)")
    win.geometry("420x260")

    tk.Label(win, text="Título").pack()
    e_titulo = tk.Entry(win, width=40)
    e_titulo.pack(pady=4)

    tk.Label(win, text="Precio").pack()
    e_precio = tk.Entry(win, width=40)
    e_precio.pack(pady=4)

    tk.Label(win, text="Vendedor (username)").pack()
    e_vendedor = tk.Entry(win, width=40)
    e_vendedor.insert(0, "ana")
    e_vendedor.pack(pady=4)

    def on_guardar():
        cn = begin_transaction()
        try:
            new_id = publicar_producto(cn, {
                "titulo": e_titulo.get().strip(),
                "precio": e_precio.get().strip(),
                "username_vendedor": e_vendedor.get().strip(),
            })
            commit(cn)
            messagebox.showinfo("OK", f"Producto publicado (fake). id={new_id}")
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", str(ex))

    tk.Button(win, text="Guardar", command=on_guardar).pack(pady=12)
