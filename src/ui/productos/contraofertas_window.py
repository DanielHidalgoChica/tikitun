"""
Ventana para mostrar y gestionar contraofertas asociadas a un producto.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.ventas.ventas_service import consultar_contraofertas, aceptar_contraoferta, rechazar_contraoferta
from src.services.productos.consulta_service import consultar_producto

def open_gestionar_contraofertas(parent, id_producto: int):
    win = tk.Toplevel(parent)
    win.title(f"Gestionar contraofertas - Producto {id_producto}")
    win.geometry("540x360")
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

    def cargar_contraofertas():
        for item in tree.get_children():
            tree.delete(item)
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
                if isinstance(r, dict):
                    u = r.get("username") or r.get("usuario")
                    p = r.get("precio")
                elif hasattr(r, "_asdict"):
                    d = r._asdict()
                    u = d.get("username") or d.get("usuario")
                    p = d.get("precio")
                else:
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

    cargar_contraofertas()

    def aceptar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una contraoferta para aceptar.", parent=win)
            return
        u, _ = tree.item(sel[0], "values")
        cn = begin_transaction()
        try:
            prod = consultar_producto(cn, id_producto)
            vendedor = prod["username_vendedor"]
            aceptar_contraoferta(cn, id_producto, u, vendedor)
            commit(cn)
            messagebox.showinfo("Correcto", f"Contraoferta de {u} aceptada.", parent=win)
            cargar_contraofertas()
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", str(ex), parent=win)

    def rechazar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una contraoferta para rechazar.", parent=win)
            return
        u, _ = tree.item(sel[0], "values")
        cn = begin_transaction()
        try:
            rechazar_contraoferta(cn, id_producto, u)
            commit(cn)
            messagebox.showinfo("Correcto", f"Contraoferta de {u} rechazada.", parent=win)
            cargar_contraofertas()
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", str(ex), parent=win)

    btn_frame = tk.Frame(win, pady=10)
    btn_frame.pack(fill=tk.X)
    tk.Button(btn_frame, text="Aceptar", command=aceptar, bg="#4CAF50", fg="white", width=14).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Rechazar", command=rechazar, bg="#F44336", fg="white", width=14).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cerrar", command=win.destroy, width=14).pack(side=tk.RIGHT, padx=5)