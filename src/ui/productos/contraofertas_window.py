"""
Ventana mínima para mostrar las contraofertas asociadas a un producto.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from src.db.db_app import connect
from src.services.ventas.ventas_service import consultar_contraofertas


def open_mostrar_contraofertas(parent, id_producto: int):
    """Abre una ventana que lista las contraofertas para un producto.

    Args:
        parent: ventana padre
        id_producto: ID del producto cuyas contraofertas mostrar
    """
    win = tk.Toplevel(parent)
    win.title(f"Contraofertas - Producto {id_producto}")
    win.geometry("520x320")
    win.resizable(False, False)

    header = tk.Frame(win, padx=12, pady=8)
    header.pack(fill=tk.X)
    tk.Label(header, text=f"Contraofertas — Producto ID {id_producto}", font=("Arial", 12, "bold")).pack(anchor="w")

    content = tk.Frame(win, padx=12, pady=6)
    content.pack(fill=tk.BOTH, expand=True)

    cols = ("username", "precio")
    tree = ttk.Treeview(content, columns=cols, show="headings", height=10)
    tree.heading("username", text="Usuario (contraofertante)")
    tree.heading("precio", text="Precio ofrecido (€)")
    tree.column("username", width=320, anchor="w")
    tree.column("precio", width=140, anchor="e")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    vsb = ttk.Scrollbar(content, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

    lbl_info = tk.Label(win, text="", anchor="w")
    lbl_info.pack(fill=tk.X, padx=12)

    # Cargar contraofertas
    try:
        with connect() as cn:
            resultados = consultar_contraofertas(cn, id_producto)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las contraofertas: {e}", parent=win)
        win.destroy()
        return

    if not resultados:
        lbl_info.config(text="No hay contraofertas para este producto.")
    else:
        lbl_info.config(text=f"Mostrando {len(resultados)} contraoferta(s).")
        for r in resultados:
            # soportar dicts, namedtuples o tuplas (id_producto, username, precio)
            if isinstance(r, dict):
                u = r.get("username") or r.get("usuario")
                p = r.get("precio")
            elif hasattr(r, "_asdict"):
                d = r._asdict()
                u = d.get("username") or d.get("usuario")
                p = d.get("precio")
            else:
                # asumir tupla con username en idx 1 y precio en idx 2
                try:
                    u = r[1]
                    p = r[2]
                except Exception:
                    u = str(r)
                    p = ""
            try:
                p_display = f"{float(p):.2f}"
            except Exception:
                p_display = str(p)
            tree.insert("", tk.END, values=(u, p_display))

    # Botón cerrar
    btn_frame = tk.Frame(win, pady=10)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text="Cerrar", command=win.destroy, width=12).pack(padx=12)

