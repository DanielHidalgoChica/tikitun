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
    from src.services.productos.productos_service import get_info_promocion
    
    win = tk.Toplevel(parent)
    win.title("Promocionar Producto")
    win.geometry("400x350")
    win.resizable(False, False)
    
    # Cargar datos del producto y usuario
    producto = None
    saldo_actual = 0
    try:
        with connect() as cn:
            info = get_info_promocion(cn, id_producto, username_vendedor)
            producto = info["producto"]
            saldo_actual = info["saldo_usuario"]
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        win.destroy()
        return
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar datos: {e}")
        win.destroy()
        return
    
    if not producto:
        messagebox.showerror("Error", "No se pudieron cargar los datos.")
        win.destroy()
        return
    
    precio_producto = producto.get("precio", 0)
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
    
    # Verificar si ya está al máximo
    if promocion_actual >= 1:
        tk.Label(
            frame,
            text="⚠️ Este producto ya está promocionado al máximo (100%).",
            font=("Arial", 11),
            fg="orange"
        ).pack(anchor="w", pady=20)
        
        tk.Button(
            frame,
            text="Cerrar",
            command=win.destroy,
            width=10
        ).pack(pady=10)
        return
    
    # Explicación
    tk.Label(
        frame,
        text="Coste = incremento × 10% × precio",
        font=("Arial", 9, "italic"),
        fg="gray"
    ).pack(anchor="w", pady=(0, 10))
    
    # Slider para grado de promoción (empieza desde la promoción actual)
    min_grado = promocion_actual if promocion_actual else 0
    tk.Label(frame, text=f"Nuevo grado de promoción (mín. {min_grado:.0%}):", font=("Arial", 10, "bold")).pack(anchor="w")
    
    slider_frame = tk.Frame(frame)
    slider_frame.pack(fill=tk.X, pady=5)
    
    grado_var = tk.DoubleVar(value=min_grado)
    coste_label = tk.Label(frame, text="Coste: 0.00€", font=("Arial", 12))
    coste_label.pack(anchor="w", pady=5)
    
    def calcular_coste(*args):
        grado = round(grado_var.get(), 2)
        # Coste basado en el INCREMENTO
        incremento = max(0, grado - promocion_actual)
        coste = round(incremento * 0.1 * precio_producto, 2)
        coste_label.config(text=f"Coste: {coste:.2f}€ (incremento: +{incremento:.0%})")
        if coste > saldo_actual:
            coste_label.config(fg="red")
        elif coste > 0:
            coste_label.config(fg="#4CAF50")
        else:
            coste_label.config(fg="gray")
    
    slider = ttk.Scale(
        slider_frame,
        from_=min_grado,
        to=1,
        orient=tk.HORIZONTAL,
        variable=grado_var,
        length=250,
        command=calcular_coste
    )
    slider.pack(side=tk.LEFT, padx=(0, 10))
    
    grado_label = tk.Label(slider_frame, text=f"{min_grado:.0%}", width=5)
    grado_label.pack(side=tk.LEFT)
    
    def update_label(*args):
        grado = round(grado_var.get(), 2)
        grado_label.config(text=f"{grado:.0%}")
    
    grado_var.trace_add("write", update_label)
    grado_var.trace_add("write", calcular_coste)
    
    # Entrada manual (alternativa al slider)
    manual_frame = tk.Frame(frame)
    manual_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(manual_frame, text=f"O introduce manualmente ({min_grado:.2f}-1):").pack(side=tk.LEFT)
    
    grado_entry = ttk.Entry(manual_frame, width=8)
    grado_entry.pack(side=tk.LEFT, padx=10)
    
    def aplicar_manual():
        try:
            valor = float(grado_entry.get())
            if valor < min_grado:
                valor = min_grado
            elif valor > 1:
                valor = 1
            grado_var.set(valor)
        except ValueError:
            messagebox.showerror("Error", f"Introduce un número válido entre {min_grado:.2f} y 1")
    
    ttk.Button(manual_frame, text="Aplicar", command=aplicar_manual).pack(side=tk.LEFT)
    
    # Botones
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=20)
    
    def on_promocionar():
        from src.services.productos.productos_service import promocionar_producto
        
        grado = round(grado_var.get(), 2)
        
        if grado <= promocion_actual:
            messagebox.showwarning("Aviso", f"Selecciona un grado mayor que la promoción actual ({promocion_actual:.0%}).")
            return
        
        incremento = grado - promocion_actual
        coste = round(incremento * 0.1 * precio_producto, 2)
        
        if not messagebox.askyesno(
            "Confirmar promoción",
            f"¿Promocionar al {grado:.0%} por {coste:.2f}€?\n\n"
            f"Incremento: +{incremento:.0%}\n"
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


def show_promocionar_view(parent, id_producto: int, username_vendedor: str):
    """Muestra el formulario de promoción en el content_frame (vista embebida).
    
    Args:
        parent: Frame contenedor (content_frame)
        id_producto: ID del producto a promocionar
        username_vendedor: Vendedor que promociona
    """
    from src.services.productos.productos_service import get_info_promocion, promocionar_producto
    
    # Limpiar contenido anterior
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Cargar datos del producto y usuario
    producto = None
    saldo_actual = 0
    try:
        with connect() as cn:
            info = get_info_promocion(cn, id_producto, username_vendedor)
            producto = info["producto"]
            saldo_actual = info["saldo_usuario"]
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        from src.ui.productos.detalle_window import show_detalle_view
        show_detalle_view(parent, id_producto, username_vendedor)
        return
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar datos: {e}")
        from src.ui.productos.detalle_window import show_detalle_view
        show_detalle_view(parent, id_producto, username_vendedor)
        return
    
    if not producto:
        messagebox.showerror("Error", "No se pudieron cargar los datos.")
        from src.ui.productos.detalle_window import show_detalle_view
        show_detalle_view(parent, id_producto, username_vendedor)
        return
    
    precio_producto = producto.get("precio", 0)
    promocion_actual = producto.get("promocion", 0) or 0
    
    # Frame principal
    main_frame = tk.Frame(parent, bg="white", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header con botón volver
    header = tk.Frame(main_frame, bg="white")
    header.pack(fill=tk.X, pady=(0, 20))
    
    def on_volver():
        from src.ui.productos.detalle_window import show_detalle_view
        show_detalle_view(parent, id_producto, username_vendedor)
    
    tk.Button(
        header,
        text="← Volver",
        command=on_volver,
        relief=tk.FLAT,
        font=("Arial", 10)
    ).pack(side=tk.LEFT)
    
    tk.Label(
        header,
        text="🚀 Promocionar Producto",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(side=tk.LEFT, padx=20)
    
    # Contenido
    content = tk.Frame(main_frame, bg="white")
    content.pack(fill=tk.BOTH, expand=True)
    
    # Título del producto
    tk.Label(
        content,
        text=producto.get("titulo", "Producto"),
        font=("Arial", 14, "bold"),
        bg="white",
        wraplength=500
    ).pack(anchor="w", pady=(0, 15))
    
    # Info actual
    info_frame = tk.Frame(content, bg="#f5f5f5", padx=15, pady=10)
    info_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(info_frame, text=f"Precio del producto: {precio_producto:.2f}€", bg="#f5f5f5").pack(anchor="w")
    tk.Label(
        info_frame,
        text=f"Tu saldo actual: {saldo_actual:.2f}€",
        bg="#f5f5f5",
        fg="#4CAF50" if saldo_actual > 0 else "red"
    ).pack(anchor="w")
    
    if promocion_actual > 0:
        tk.Label(info_frame, text=f"Promoción actual: {promocion_actual:.0%}", bg="#f5f5f5", fg="orange").pack(anchor="w")
    
    # Verificar si ya está al máximo
    if promocion_actual >= 1:
        tk.Label(
            content,
            text="⚠️ Este producto ya está promocionado al máximo (100%).",
            font=("Arial", 11),
            bg="white",
            fg="orange"
        ).pack(anchor="w", pady=20)
        
        tk.Button(content, text="Volver", command=on_volver, width=10).pack(pady=10)
        return
    
    # Explicación
    tk.Label(
        content,
        text="Coste = incremento × 10% × precio",
        font=("Arial", 9, "italic"),
        fg="gray",
        bg="white"
    ).pack(anchor="w", pady=(0, 10))
    
    # Slider
    min_grado = promocion_actual
    tk.Label(content, text=f"Nuevo grado de promoción (mín. {min_grado:.0%}):", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
    
    slider_frame = tk.Frame(content, bg="white")
    slider_frame.pack(fill=tk.X, pady=5)
    
    grado_var = tk.DoubleVar(value=min_grado)
    coste_label = tk.Label(content, text="Coste: 0.00€", font=("Arial", 12), bg="white")
    coste_label.pack(anchor="w", pady=5)
    
    def calcular_coste(*args):
        grado = round(grado_var.get(), 2)
        incremento = max(0, grado - promocion_actual)
        coste = round(incremento * 0.1 * precio_producto, 2)
        coste_label.config(text=f"Coste: {coste:.2f}€ (incremento: +{incremento:.0%})")
        if coste > saldo_actual:
            coste_label.config(fg="red")
        elif coste > 0:
            coste_label.config(fg="#4CAF50")
        else:
            coste_label.config(fg="gray")
    
    slider = ttk.Scale(slider_frame, from_=min_grado, to=1, orient=tk.HORIZONTAL, variable=grado_var, length=300, command=calcular_coste)
    slider.pack(side=tk.LEFT, padx=(0, 10))
    
    grado_label = tk.Label(slider_frame, text=f"{min_grado:.0%}", width=5, bg="white")
    grado_label.pack(side=tk.LEFT)
    
    def update_label(*args):
        grado_label.config(text=f"{grado_var.get():.0%}")
    
    grado_var.trace_add("write", update_label)
    grado_var.trace_add("write", calcular_coste)
    
    # Botones
    btn_frame = tk.Frame(content, bg="white")
    btn_frame.pack(pady=30)
    
    def on_promocionar():
        grado = round(grado_var.get(), 2)
        
        if grado <= promocion_actual:
            messagebox.showwarning("Aviso", f"Selecciona un grado mayor que {promocion_actual:.0%}.")
            return
        
        incremento = grado - promocion_actual
        coste = round(incremento * 0.1 * precio_producto, 2)
        
        if not messagebox.askyesno(
            "Confirmar",
            f"¿Promocionar al {grado:.0%} por {coste:.2f}€?\nIncremento: +{incremento:.0%}"
        ):
            return
        
        cn = begin_transaction()
        try:
            coste_real = promocionar_producto(cn, id_producto, username_vendedor, grado)
            commit(cn)
            messagebox.showinfo("¡Promocionado!", f"Coste: {coste_real:.2f}€\nNuevo grado: {grado:.0%}")
            from src.ui.productos.detalle_window import show_detalle_view
            show_detalle_view(parent, id_producto, username_vendedor)
        except ValueError as e:
            rollback(cn)
            messagebox.showerror("Error", str(e))
        except Exception as e:
            rollback(cn)
            messagebox.showerror("Error", f"Error: {e}")
    
    tk.Button(
        btn_frame,
        text="🚀 Promocionar",
        command=on_promocionar,
        bg="#FF9800",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15
    ).pack(side=tk.LEFT, padx=10)
    
    tk.Button(btn_frame, text="Cancelar", command=on_volver, width=10).pack(side=tk.LEFT, padx=10)
