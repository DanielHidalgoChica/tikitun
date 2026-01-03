import tkinter as tk
from src.ui.publicar_producto_window import open_publicar_producto
from src.ui.buscar_productos_window import open_buscar_productos
from src.ui.abrir_chat_window import open_abrir_chat
from src.ui.enviar_mensaje_window import open_enviar_mensaje

def run_app():
    root = tk.Tk()
    root.title("TikiTun Demo (esqueleto)")
    root.geometry("520x320")

    tk.Label(root, text="TikiTun - MiniDemo (sin implementación real)", font=("Arial", 14)).pack(pady=12)

    tk.Button(root, text="Publicar producto", width=30, command=lambda: open_publicar_producto(root)).pack(pady=6)
    tk.Button(root, text="Buscar productos", width=30, command=lambda: open_buscar_productos(root)).pack(pady=6)
    tk.Button(root, text="Abrir chat", width=30, command=lambda: open_abrir_chat(root)).pack(pady=6)
    tk.Button(root, text="Enviar mensaje", width=30, command=lambda: open_enviar_mensaje(root)).pack(pady=6)

    tk.Label(root, text="Mira la consola: verás BEGIN/COMMIT/ROLLBACK y llamadas por capas.").pack(pady=12)

    root.mainloop()
