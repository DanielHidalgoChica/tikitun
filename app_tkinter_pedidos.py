# ------------------------------------------------------------
# app_tkinter_pedidos.py — GUI secuencial para el Seminario
#   Ventana principal  ->  Ventana "Alta de pedido"
#   Control transaccional: SAVEPOINT, ROLLBACK, COMMIT
# ------------------------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import date
import pandas as pd

from db_app import (
    ORACLE_HOST, ORACLE_PORT, ORACLE_SERVICE, ORACLE_USER,
    reset_schema, fetch_all_tables, begin_transaction, commit_transaction,
    rollback_transaction, savepoint, insert_pedido, insert_detalle,
    delete_detalles_via_savepoint, cancel_pedido,
)

APP_TITLE = "Seminario BD · Mini SI (Oracle + Tkinter)"
SAVEPOINT_CAB = "CAB"


# ---------------------------
# Ventana de alta de pedido
# ---------------------------
class AltaPedidoWindow(tk.Toplevel):
    def __init__(self, master, on_finish):
        super().__init__(master)
        self.title("Alta de pedido (transacción activa)")
        self.geometry("1200x650")
        self.on_finish = on_finish

        # Conexión/transacción viva para toda la ventana
        try:
            self.cn = begin_transaction()
        except Exception as e:
            messagebox.showerror("Conexión", f"No se pudo abrir transacción:\n{e}")
            self.destroy()
            return

        # --- Cabecera del pedido ---
        frm_head = ttk.LabelFrame(self, text="Cabecera de pedido")
        frm_head.pack(fill="x", padx=10, pady=10)

        ttk.Label(frm_head, text="Cpedido:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(frm_head, text="Ccliente:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        ttk.Label(frm_head, text="Fecha (YYYY-MM-DD):").grid(row=0, column=4, sticky="e", padx=5, pady=5)

        self.var_cpedido = tk.StringVar()
        self.var_ccliente = tk.StringVar()
        self.var_fecha = tk.StringVar(value=str(date.today()))

        ttk.Entry(frm_head, textvariable=self.var_cpedido, width=10).grid(row=0, column=1, padx=5, pady=5)
        ttk.Entry(frm_head, textvariable=self.var_ccliente, width=10).grid(row=0, column=3, padx=5, pady=5)
        ttk.Entry(frm_head, textvariable=self.var_fecha, width=12).grid(row=0, column=5, padx=5, pady=5)

        self.btn_crear = ttk.Button(frm_head, text="Crear pedido (INSERT + SAVEPOINT)", command=self._crear_pedido)
        self.btn_crear.grid(row=0, column=6, padx=10, pady=5)
        self.btn_salir = ttk.Button(frm_head, text="Salir sin crear pedido", command=self._close_and_return)
        self.btn_salir.grid(row=0, column=7, padx=10, pady=5)

        # --- Zona de operaciones de detalle ---
        frm_ops = ttk.LabelFrame(self, text="Operaciones (1- Añadir detalle, 2- Eliminar detalles, 3- Cancelar, 4- Finalizar)")
        frm_ops.pack(fill="x", padx=10, pady=10)

        ttk.Label(frm_ops, text="Cproducto:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(frm_ops, text="Cantidad:").grid(row=0, column=2, sticky="e", padx=5, pady=5)

        self.var_cproducto = tk.StringVar()
        self.var_cantidad = tk.StringVar()

        self.ent_cprod = ttk.Entry(frm_ops, textvariable=self.var_cproducto, width=10, state="disabled")
        self.ent_cant = ttk.Entry(frm_ops, textvariable=self.var_cantidad, width=10, state="disabled")
        self.ent_cprod.grid(row=0, column=1, padx=5, pady=5)
        self.ent_cant.grid(row=0, column=3, padx=5, pady=5)

        self.btn_add = ttk.Button(frm_ops, text="1) Añadir detalle", command=self._add_detalle, state="disabled")
        self.btn_del_all = ttk.Button(frm_ops, text="2) Eliminar TODOS los detalles", command=self._del_todos, state="disabled")
        self.btn_cancel = ttk.Button(frm_ops, text="3) Cancelar pedido (ROLLBACK)", command=self._cancelar, state="disabled")
        self.btn_commit = ttk.Button(frm_ops, text="4) Finalizar pedido (COMMIT)", command=self._finalizar, state="disabled")

        self.btn_add.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.btn_del_all.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.btn_cancel.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.btn_commit.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # --- Salida / estado BD ---
        ttk.Label(self, text="Contenido de las tablas (incluye cambios no confirmados):",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10)
        self.txt = ScrolledText(self, height=22)
        self.txt.pack(fill="both", expand=True, padx=10, pady=8)

        # Estado interno
        self.pedido_creado = False
        self.current_cpedido = None

        self._print_bd()

        # Al cerrar la ventana, preguntar si hay transacción abierta
        self.protocol("WM_DELETE_WINDOW", self._on_close) #Cuando se cierra la ventana desde el windows manager (la X de cerrar), se sobreescribe el protocolo por defecto para que llame a _on_close

    # --- Acciones ---
    def _crear_pedido(self):
        try:
            cpedido = int(self.var_cpedido.get())
            ccliente = int(self.var_ccliente.get())
            fecha = date.fromisoformat(self.var_fecha.get())
        except Exception:
            messagebox.showwarning("Datos", "Revisa Cpedido, Ccliente y Fecha.")
            return

        try:
            insert_pedido(self.cn, cpedido, ccliente, fecha)
            savepoint(self.cn, SAVEPOINT_CAB)  # savepoint tras cabecera
            self.pedido_creado = True
            self.current_cpedido = cpedido

            # Habilitar operaciones 1..4
            for w in (self.ent_cprod, self.ent_cant, self.btn_add, self.btn_del_all, self.btn_cancel, self.btn_commit):
                w.configure(state="normal")
            # Deshabilitar crear pedido
            self.btn_crear.configure(state="disabled")
            # Deshabilitar salir sin crear pedido
            self.btn_salir.configure(state="disabled")
            messagebox.showinfo("Pedido", f"Cabecera creada (CPEDIDO={cpedido}). Savepoint '{SAVEPOINT_CAB}' establecido.")
            self._print_bd()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el pedido:\n{e}")
            self._print_bd()

    def _add_detalle(self):
        if not self.pedido_creado:
            return
        try:
            cproducto = int(self.var_cproducto.get())
            cantidad = int(self.var_cantidad.get())
        except Exception:
            messagebox.showwarning("Datos", "Revisa Cproducto y Cantidad.")
            return

        try:
            insert_detalle(self.cn, self.current_cpedido, cproducto, cantidad)
            messagebox.showinfo("Detalle", f"Detalle añadido (CPRODUCTO={cproducto}, CANTIDAD={cantidad}).")
            self._print_bd()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir el detalle:\n{e}")
            self._print_bd()

    def _del_todos(self):
        if not self.pedido_creado:
            return
        try:
            # Volver al savepoint de cabecera => borra detalles y revierte stocks
            delete_detalles_via_savepoint(self.cn, SAVEPOINT_CAB)
            messagebox.showinfo("Detalles", "Se han eliminado TODOS los detalles del pedido (ROLLBACK TO SAVEPOINT).")
            self._print_bd()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar los detalles:\n{e}")
            self._print_bd()

    def _cancelar(self):
        if not self.pedido_creado:
            return
        try:
            cancel_pedido(self.cn)  # rollback total
            messagebox.showinfo("Cancelar", "Transacción cancelada (ROLLBACK).")
            self._close_and_return()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cancelar la transacción:\n{e}")
            self._print_bd()

    def _finalizar(self):
        if not self.pedido_creado:
            return
        try:
            commit_transaction(self.cn)
            messagebox.showinfo("Finalizar", "Transacción confirmada (COMMIT).")
            self._close_and_return()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo confirmar la transacción:\n{e}")
            self._print_bd()

    # --- Utilidades UI ---
    def _print_bd(self):
        try:
            data = fetch_all_tables(self.cn)  # leer con la misma transacción que está activa ahora mismo

            #TODO: Esto es codigo repe con el _mostrar, habría que hacer una funcion que parsee el texto
            #Porque es el mas comun y nos parecia el mas comodo por aprovechar lubrerias como tkinter
            self.txt.delete("1.0", tk.END)
            for name in ["STOCK", "PEDIDO", "DETALLE_PEDIDO"]:
                self.txt.insert(tk.END, f"\n=== {name} ===\n")
                rows = data.get(name, [])
                if rows:
                    df = pd.DataFrame(rows)
                    self.txt.insert(tk.END, df.to_string(index=False))
                else:
                    self.txt.insert(tk.END, "(vacía)\n")
                self.txt.insert(tk.END, "\n" + "-" * 50 + "\n")
        except Exception as e:
            messagebox.showerror("Consulta", f"Error al listar tablas:\n{e}")

    def _close_and_return(self):
        try:
            self.cn.close()
        except Exception:
            pass
        self.on_finish()
        self.destroy()

    def _on_close(self):
        # Si el usuario cierra la ventana con la transacción viva, prevenir fuga
        if self.pedido_creado:
            if messagebox.askyesno("Cerrar", "Hay una transacción abierta.\n¿Cancelar (ROLLBACK) y cerrar?"):
                try:
                    rollback_transaction(self.cn)
                except Exception:
                    pass
                self._close_and_return()
            else:
                return
        else:
            try:
                self.cn.close()
            except Exception:
                pass
            self.destroy()


# ---------------------------
# Ventana principal
# ---------------------------
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("950x700")

        # Parámetros conexión (solo lectura)
        frame_conn = ttk.LabelFrame(self, text="Parámetros de conexión (solo lectura)")
        frame_conn.pack(fill="x", padx=10, pady=10)
        info = f"HOST: {ORACLE_HOST}   PORT: {ORACLE_PORT}   SERVICE: {ORACLE_SERVICE}   USER: {ORACLE_USER}"
        ttk.Label(frame_conn, text=info).pack(anchor="w", padx=10, pady=5)

        # Menú principal
        frame_menu = ttk.LabelFrame(self, text="Menú principal")
        frame_menu.pack(fill="x", padx=10, pady=10)

        ttk.Button(frame_menu, text="🔁 Borrado y creación de tablas + 10 filas STOCK", command=self._resetear).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_menu, text="🛒 Dar de alta nuevo pedido", command=self._alta_pedido).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_menu, text="👁️ Mostrar contenido de tablas", command=self._mostrar).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_menu, text="🚪 Salir", command=self.destroy).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Salida
        ttk.Label(self, text="Salida:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10)
        self.txt = ScrolledText(self, height=26)
        self.txt.pack(fill="both", expand=True, padx=10, pady=8)

    # Acciones
    def _resetear(self):
        try:
            reset_schema()
            messagebox.showinfo("BD", "Esquema reiniciado e inicializado (10 filas en STOCK).")
            self._mostrar()
        except Exception as e:
            messagebox.showerror("BD", f"Error al resetear:\n{e}")

    def _alta_pedido(self):
        def on_finish():
            # Al cerrar ventana de pedido, refrescar salida
            self._mostrar()
        AltaPedidoWindow(self, on_finish)

    def _mostrar(self):
        try:
            data = fetch_all_tables() #AQUI NO LE PASAMOS CONECTION (ventana principal, la crea el)
            self.txt.delete("1.0", tk.END)
            for name in ["STOCK", "PEDIDO", "DETALLE_PEDIDO"]:
                self.txt.insert(tk.END, f"\n=== {name} ===\n")
                rows = data.get(name, [])
                if rows:
                    df = pd.DataFrame(rows)
                    self.txt.insert(tk.END, df.to_string(index=False))
                else:
                    self.txt.insert(tk.END, "(vacía)\n")
                self.txt.insert(tk.END, "\n" + "-" * 50 + "\n")
        except Exception as e:
            messagebox.showerror("Consulta", f"Error al listar tablas:\n{e}")


if __name__ == "__main__":
    MainWindow().mainloop()
