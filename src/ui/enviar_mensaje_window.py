import tkinter as tk
from tkinter import messagebox
from src.db.db_app import begin_transaction, commit, rollback
from src.services.mensajes_service import enviar_mensaje

def open_enviar_mensaje(parent):
    win = tk.Toplevel(parent)
    win.title("Enviar mensaje (stub)")
    win.geometry("520x300")

    tk.Label(win, text="ID Chat").pack()
    e_chat = tk.Entry(win, width=50)
    e_chat.insert(0, "10")
    e_chat.pack(pady=4)

    tk.Label(win, text="Emisor (username)").pack()
    e_emisor = tk.Entry(win, width=50)
    e_emisor.insert(0, "pepe")
    e_emisor.pack(pady=4)

    tk.Label(win, text="Texto").pack()
    e_txt = tk.Entry(win, width=50)
    e_txt.pack(pady=6)

    def on_send():
        cn = begin_transaction()
        try:
            mid = enviar_mensaje(cn, {
                "id_chat": int(e_chat.get().strip()),
                "username_emisor": e_emisor.get().strip(),
                "texto": e_txt.get().strip(),
            })
            commit(cn)
            messagebox.showinfo("OK", f"Mensaje enviado (fake). id_mensaje={mid}")
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", str(ex))

    tk.Button(win, text="Enviar", command=on_send).pack(pady=12)
