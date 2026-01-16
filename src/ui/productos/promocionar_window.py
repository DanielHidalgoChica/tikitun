"""
Ventana de promoción de producto (RF2.5).
Permite al vendedor promocionar su producto pagando desde el monedero.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.db.db_app import connect, begin_transaction, commit, rollback


def open_promocionar_producto(parent, id_producto: int, username_vendedor: str):
    """Abre una ventana para promocionar un producto.
    
    Args:
        parent: Ventana padre
        id_producto: ID del producto a promocionar
        username_vendedor: Vendedor que promociona
    """
    from src.services.productos.productos_service import consultar_producto
    from src.repositories.perfiles.usuarios_repo import get_usuario
    
    win = tk.Toplevel(parent)
    win.title("Promocionar Producto")
    win.geometry("400x350")
    win.resizable(False, False)
    
    # Cargar datos del producto y usuario
    producto = None
    usuario = None
    try:
        with connect() as cn:
            producto = consultar_producto(cn, id_producto)
            usuario = get_usuario(cn, username_vendedor)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        win.destroy()
        return
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar datos: {e}")
        win.destroy()
        return
    
    if not producto or not usuario:
        messagebox.showerror("Error", "No se pudieron cargar los datos.")
        win.destroy()
        return
    
    precio_producto = producto.get("precio", 0)
    saldo_actual = usuario.get("saldo", 0)
    promocion_actual = producto.get("promocion", 0)
    
    # --- Contenido ---
    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Título del producto
    tk.Label(
        frame,
        text=producto.get("titulo", "Producto"),
        font=("Arial", 14, "bold"),
        wraplength=350
    ).pack(anchor="w", pady=(0, 15))
    
    # Info actual
    info_frame = tk.Frame(frame, bg="#f5f5f5", padx=10, pady=10)
    info_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(
        info_frame,
        text=f"Precio del producto: {precio_producto:.2f}€",
        bg="#f5f5f5"
    ).pack(anchor="w")
    
    tk.Label(
        info_frame,
        text=f"Tu saldo actual: {saldo_actual:.2f}€",
        bg="#f5f5f5",
        fg="#4CAF50" if saldo_actual > 0 else "red"
    ).pack(anchor="w")
    
    if promocion_actual and promocion_actual > 0:
        tk.Label(
            info_frame,
            text=f"Promoción actual: {promocion_actual:.0%}",
            bg="#f5f5f5",
            fg="orange"
        ).pack(anchor="w")
    
    # Explicación
    tk.Label(
        frame,
        text="Coste = grado × 10% × precio",
        font=("Arial", 9, "italic"),
        fg="gray"
    ).pack(anchor="w", pady=(0, 10))
    
    # Slider para grado de promoción
    tk.Label(frame, text="Grado de promoción:", font=("Arial", 10, "bold")).pack(anchor="w")
    
    slider_frame = tk.Frame(frame)
    slider_frame.pack(fill=tk.X, pady=5)
    
    grado_var = tk.DoubleVar(value=0)
    coste_label = tk.Label(frame, text="Coste: 0.00€", font=("Arial", 12))
    coste_label.pack(anchor="w", pady=5)
    
    def calcular_coste(*args):
        grado = round(grado_var.get(), 2)
        coste = round(grado * 0.1 * precio_producto, 2)
        coste_label.config(text=f"Coste: {coste:.2f}€")
        if coste > saldo_actual:
            coste_label.config(fg="red")
        else:
            coste_label.config(fg="#4CAF50")
    
    slider = ttk.Scale(
        slider_frame,
        from_=0,
        to=1,
        orient=tk.HORIZONTAL,
        variable=grado_var,
        length=250,
        command=calcular_coste
    )
    slider.pack(side=tk.LEFT, padx=(0, 10))
    
    grado_label = tk.Label(slider_frame, text="0%", width=5)
    grado_label.pack(side=tk.LEFT)
    
    def update_label(*args):
        grado = round(grado_var.get(), 2)
        grado_label.config(text=f"{grado:.0%}")
    
    grado_var.trace_add("write", update_label)
    grado_var.trace_add("write", calcular_coste)
    
    # Entrada manual (alternativa al slider)
    manual_frame = tk.Frame(frame)
    manual_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(manual_frame, text="O introduce manualmente (0-1):").pack(side=tk.LEFT)
    
    grado_entry = ttk.Entry(manual_frame, width=8)
    grado_entry.pack(side=tk.LEFT, padx=10)
    
    def aplicar_manual():
        try:
            valor = float(grado_entry.get())
            if valor < 0:
                valor = 0
            elif valor > 1:
                valor = 1
            grado_var.set(valor)
        except ValueError:
            messagebox.showerror("Error", "Introduce un número válido entre 0 y 1")
    
    ttk.Button(manual_frame, text="Aplicar", command=aplicar_manual).pack(side=tk.LEFT)
    
    # Botones
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=20)
    
    def on_promocionar():
        from src.services.productos.productos_service import promocionar_producto
        
        grado = round(grado_var.get(), 2)
        
        if grado <= 0:
            messagebox.showwarning("Aviso", "Selecciona un grado de promoción mayor que 0.")
            return
        
        coste = round(grado * 0.1 * precio_producto, 2)
        
        if not messagebox.askyesno(
            "Confirmar promoción",
            f"¿Promocionar al {grado:.0%} por {coste:.2f}€?\n\n"
            f"Se descontará de tu monedero."
        ):
            return
        
        cn = begin_transaction()
        try:
            coste_real = promocionar_producto(cn, id_producto, username_vendedor, grado)
            commit(cn)
            messagebox.showinfo(
                "¡Promocionado!",
                f"Tu producto ha sido promocionado.\n"
                f"Coste: {coste_real:.2f}€\n"
                f"Nuevo grado: {grado:.0%}"
            )
            win.destroy()
            # Refrescar la ventana padre si es posible
            if hasattr(parent, 'destroy'):
                try:
                    from src.ui.productos.detalle_window import show_detalle_producto
                    parent.destroy()
                    # Reabrir detalle actualizado
                    if parent.master:
                        show_detalle_producto(parent.master, id_producto, username_vendedor)
                except:
                    pass
        except ValueError as e:
            rollback(cn)
            messagebox.showerror("Error", str(e))
        except Exception as e:
            rollback(cn)
            messagebox.showerror("Error", f"Error al promocionar: {e}")
    
    tk.Button(
        btn_frame,
        text="🚀 Promocionar",
        command=on_promocionar,
        bg="#FF9800",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15
    ).pack(side=tk.LEFT, padx=10)
    
    tk.Button(
        btn_frame,
        text="Cancelar",
        command=win.destroy,
        width=10
    ).pack(side=tk.LEFT, padx=10)
