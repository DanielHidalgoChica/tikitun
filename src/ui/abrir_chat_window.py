import tkinter as tk
from tkinter import messagebox
from src.db.db_app import begin_transaction, commit, rollback
from src.services.chats_service import abrir_chat

def open_abrir_chat(parent):
    win = tk.Toplevel(parent)
    win.title("Abrir chat (stub)")
    win.geometry("420x280")

    tk.Label(win, text="ID Producto").pack()
    e_prod = tk.Entry(win, width=40)
    e_prod.insert(0, "1")
    e_prod.pack(pady=4)

    tk.Label(win, text="Comprador (username)").pack()
    e_comp = tk.Entry(win, width=40)
    e_comp.insert(0, "pepe")
    e_comp.pack(pady=4)

    tk.Label(win, text="Vendedor (username)").pack()
    e_vend = tk.Entry(win, width=40)
    e_vend.insert(0, "ana")
    e_vend.pack(pady=4)

    def on_abrir():
        cn = begin_transaction()
        try:
            chat_id = abrir_chat(cn, {
                "id_producto": int(e_prod.get().strip()),
                "username_comprador": e_comp.get().strip(),
                "username_vendedor": e_vend.get().strip(),
            })
            commit(cn)
            messagebox.showinfo("OK", f"Chat abierto (fake). id_chat={chat_id}")
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", str(ex))

    tk.Button(win, text="Abrir chat", command=on_abrir).pack(pady=12)
