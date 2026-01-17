"""
Vista de gestión de monedero del usuario.
Implementa RF1.4: Añadir saldo al monedero.
Implementa RF1.5: Transferir saldo a cuenta bancaria.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.repositories.perfiles import usuarios_repo


def show_monedero_view(parent_frame, username: str):
    """Muestra la vista de gestión de monedero.
    
    Args:
        parent_frame: Frame contenedor (content_frame)
        username: Usuario actual
    """
    # Limpiar contenido anterior
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Frame principal
    frame = tk.Frame(parent_frame, bg="white", padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    tk.Label(
        frame,
        text="💰 Gestionar Monedero",
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=(0, 20))
    
    # Cargar datos del usuario
    try:
        with connect() as cn:
            usuario = usuarios_repo.get_usuario(cn, username)
            if not usuario:
                messagebox.showerror("Error", "Usuario no encontrado")
                return
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando datos: {e}")
        return
    
    saldo_actual = usuario.get("saldo", 0.0)
    
    # === INFORMACIÓN DE SALDO ===
    frm_saldo = tk.LabelFrame(
        frame,
        text="Saldo Actual",
        padx=20,
        pady=20,
        bg="white"
    )
    frm_saldo.pack(fill=tk.X, pady=10)
    
    tk.Label(
        frm_saldo,
        text=f"€ {saldo_actual:.2f}",
        font=("Arial", 24, "bold"),
        bg="white",
        fg="#4CAF50"
    ).pack()
    
    # === TABS PARA RECARGA Y RETIRADA ===
    notebook = ttk.Notebook(frame)
    notebook.pack(fill=tk.BOTH, pady=5)
    
    # TAB 1: RECARGA
    tab_recarga = tk.Frame(notebook, bg="white", padx=20, pady=20)
    notebook.add(tab_recarga, text="➕ Recarga")
    
    crear_tab_recarga(tab_recarga, username, parent_frame, saldo_actual)
    
    # TAB 2: RETIRADA
    tab_retirada = tk.Frame(notebook, bg="white", padx=20, pady=20)
    notebook.add(tab_retirada, text="➖ Retirada")
    
    crear_tab_retirada(tab_retirada, username, parent_frame, saldo_actual)
    
    # Botón volver
    tk.Button(
        frame,
        text="⬅️ Volver al Perfil",
        command=lambda: volver_a_perfil(parent_frame, username),
        bg="#607D8B",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=20,
        pady=5
    ).pack()


def crear_tab_recarga(parent, username: str, content_frame, saldo_actual: float):
    """Crea el tab de recarga de saldo (RF1.4).
    
    Args:
        parent: Frame padre
        username: Usuario actual
        content_frame: Frame de contenido para actualizaciones
        saldo_actual: Saldo actual del usuario
    """
    tk.Label(
        parent,
        text="Añadir saldo a tu monedero",
        font=("Arial", 12, "bold"),
        bg="white"
    ).pack(pady=(0, 5))
    
    # Opciones predefinidas
    tk.Label(parent, text="Selecciona una cantidad:", font=("Arial", 10), bg="white").pack(anchor="w", pady=(0, 5))
    
    frm_opciones = tk.Frame(parent, bg="white")
    frm_opciones.pack(fill=tk.X, pady=5)
    
    cantidad_var = tk.StringVar()
    opciones = [10, 25, 50, 100]
    
    for cantidad in opciones:
        tk.Radiobutton(
            frm_opciones,
            text=f"€ {cantidad:.2f}",
            variable=cantidad_var,
            value=str(cantidad),
            bg="white"
        ).pack(anchor="w", pady=5)
    
    # Cantidad personalizada
    tk.Label(parent, text="O ingresa una cantidad personalizada:", font=("Arial", 10), bg="white").pack(anchor="w", pady=(20, 10))
    
    frm_personalizado = tk.Frame(parent, bg="white")
    frm_personalizado.pack(fill=tk.X, pady=10)
    
    tk.Label(frm_personalizado, text="€", bg="white").pack(side=tk.LEFT, padx=(0, 5))
    cantidad_personalizada_var = tk.StringVar()
    entry_personalizado = tk.Entry(frm_personalizado, textvariable=cantidad_personalizada_var, width=15)
    entry_personalizado.pack(side=tk.LEFT, padx=(0, 5))
    
    # Vincular entrada personalizada
    def seleccionar_personalizado(*args):
        cantidad_var.set("")
    
    cantidad_personalizada_var.trace("w", seleccionar_personalizado)
    
    def procesar_recarga():
        """Procesa la recarga de saldo."""
        # Obtener cantidad
        cantidad_str = cantidad_var.get() or cantidad_personalizada_var.get()
        
        if not cantidad_str:
            messagebox.showerror("Error", "Debes seleccionar o ingresar una cantidad")
            return
        
        try:
            cantidad = float(cantidad_str)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser positiva")
                return
            
            # Validar máximo 2 decimales
            if len(str(cantidad).split(".")[-1]) > 2:
                messagebox.showerror("Error", "Máximo 2 decimales permitidos")
                return
                
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return
        
        # Confirmar operación
        if not messagebox.askyesno(
            "Confirmar Recarga",
            f"¿Deseas añadir € {cantidad:.2f} a tu monedero?\n\n"
            f"Saldo actual: € {saldo_actual:.2f}\n"
            f"Nuevo saldo: € {saldo_actual + cantidad:.2f}"
        ):
            return
        
        # Realizar transacción
        cn = begin_transaction()
        try:
            usuario_actual = usuarios_repo.get_usuario(cn, username)
            if not usuario_actual:
                messagebox.showerror("Error", "Usuario no encontrado")
                rollback(cn)
                return
            
            nuevo_saldo = usuario_actual.get("saldo", 0.0) + cantidad
            usuarios_repo.update_saldo(cn, username, nuevo_saldo)
            commit(cn)
            
            messagebox.showinfo(
                "Éxito",
                f"Recarga realizada correctamente.\n\n"
                f"Nuevo saldo: € {nuevo_saldo:.2f}"
            )
            
            # Refrescar vista
            show_monedero_view(content_frame, username)
            
        except Exception as e:
            rollback(cn)
            messagebox.showerror("Error", f"Error en la transacción: {e}")
    
    tk.Button(
        parent,
        text="✅ Confirmar Recarga",
        command=procesar_recarga,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=20,
        pady=10
    ).pack(pady=20, fill=tk.X)


def crear_tab_retirada(parent, username: str, content_frame, saldo_actual: float):
    """Crea el tab de retirada de saldo (RF1.5).
    
    Args:
        parent: Frame padre
        username: Usuario actual
        content_frame: Frame de contenido para actualizaciones
        saldo_actual: Saldo actual del usuario
    """
    tk.Label(
        parent,
        text="Transferir saldo a cuenta bancaria",
        font=("Arial", 12, "bold"),
        bg="white"
    ).pack(pady=(0, 20))
    
    # Cantidad
    tk.Label(parent, text="Cantidad a transferir:", font=("Arial", 10), bg="white").pack(anchor="w", pady=(0, 5))
    frm_cantidad = tk.Frame(parent, bg="white")
    frm_cantidad.pack(fill=tk.X, pady=10)
    tk.Label(frm_cantidad, text="€", bg="white").pack(side=tk.LEFT, padx=(0, 5))
    cantidad_var = tk.StringVar()
    tk.Entry(frm_cantidad, textvariable=cantidad_var, width=15).pack(side=tk.LEFT)
    
    # Contraseña
    tk.Label(parent, text="Contraseña (confirmación):", font=("Arial", 10), bg="white").pack(anchor="w", pady=(20, 5))
    contraseña_var = tk.StringVar()
    tk.Entry(parent, textvariable=contraseña_var, show="*", width=20).pack(anchor="w", padx=10, pady=(0, 20))
    
    # Información de saldo
    frm_info = tk.Frame(parent, bg="white")
    frm_info.pack(fill=tk.X, pady=10)
    tk.Label(frm_info, text=f"Saldo disponible: € {saldo_actual:.2f}", font=("Arial", 9), bg="white", fg="gray").pack(anchor="w")
    
    def procesar_retirada():
        """Procesa la retirada de saldo."""
        # Validar cantidad
        cantidad_str = cantidad_var.get().strip()
        if not cantidad_str:
            messagebox.showerror("Error", "Debes ingresar una cantidad")
            return
        
        try:
            cantidad = float(cantidad_str)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser positiva")
                return
            
            # Validar máximo 2 decimales
            if len(str(cantidad).split(".")[-1]) > 2:
                messagebox.showerror("Error", "Máximo 2 decimales permitidos")
                return
                
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return
        
        # Validar contraseña
        contraseña = contraseña_var.get()
        if not contraseña:
            messagebox.showerror("Error", "Debes ingresar tu contraseña")
            return
        
        if not (8 <= len(contraseña) <= 15):
            messagebox.showerror("Error", "La contraseña debe tener entre 8 y 15 caracteres")
            return
        
        # Validar saldo
        if cantidad > saldo_actual:
            messagebox.showerror("Error", "Saldo insuficiente")
            return
        
        # Confirmar operación
        if not messagebox.askyesno(
            "Confirmar Retirada",
            f"¿Deseas transferir € {cantidad:.2f} a tu cuenta bancaria?\n\n"
            f"Saldo actual: € {saldo_actual:.2f}\n"
            f"Saldo después: € {saldo_actual - cantidad:.2f}"
        ):
            return
        
        # Realizar transacción
        cn = begin_transaction()
        try:
            usuario_actual = usuarios_repo.get_usuario(cn, username)
            if not usuario_actual:
                messagebox.showerror("Error", "Usuario no encontrado")
                rollback(cn)
                return
            
            # Verificar contraseña
            if not usuarios_repo.verificar_contraseña(cn, username, contraseña):
                rollback(cn)
                messagebox.showerror("Error", "Contraseña incorrecta")
                return
            
            # Verificar saldo disponible
            saldo_bd = usuario_actual.get("saldo", 0.0)
            if cantidad > saldo_bd:
                rollback(cn)
                messagebox.showerror("Error", "Saldo insuficiente")
                return
            
            nuevo_saldo = saldo_bd - cantidad
            usuarios_repo.update_saldo(cn, username, nuevo_saldo)
            commit(cn)
            
            messagebox.showinfo(
                "Éxito",
                f"Transferencia realizada correctamente.\n\n"
                f"Cantidad transferida: € {cantidad:.2f}\n"
                f"Nuevo saldo: € {nuevo_saldo:.2f}"
            )
            
            # Refrescar vista
            show_monedero_view(content_frame, username)
            
        except Exception as e:
            rollback(cn)
            messagebox.showerror("Error", f"Error en la transacción: {e}")
    
    tk.Button(
        parent,
        text="✅ Confirmar Retirada",
        command=procesar_retirada,
        bg="#FF9800",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=20,
        pady=10
    ).pack(pady=20, fill=tk.X)


def volver_a_perfil(parent_frame, username: str):
    """Vuelve a la vista de perfil."""
    from src.ui.perfil.perfil_window import show_perfil_view
    show_perfil_view(parent_frame, username)
