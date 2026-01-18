import tkinter as tk
from tkinter import messagebox, ttk
from src.db.db_app import connect
from src.services.perfiles import usuarios_service


def show_perfil_view(parent_frame, username, current_user=None):
    """
    Muestra la vista de gestión de perfil (RF1.2).
    
    Args:
        parent_frame: Frame padre donde se muestra la vista
        username: Usuario del perfil a consultar
        current_user: Usuario actualmente logueado (si es None, se asume que es el mismo que username)
    
    Consulta:
    - Información del perfil del usuario
    """
    # Si no se especifica current_user, asumimos que es el propio usuario
    if current_user is None:
        current_user = username
    
    es_mi_perfil = (username == current_user)
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Cargar datos del usuario
    try:
        with connect() as cn:
            usuario = usuarios_service.get_usuario(cn, username)
            if usuario is None or usuario.get("cuenta_eliminada"):
                messagebox.showerror("Error", "El usuario no existe o ha sido eliminado")
                tk.Label(parent_frame, text="Usuario no encontrado").pack(pady=20)
                return
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando perfil: {e}")
        tk.Label(parent_frame, text="Error al cargar el perfil").pack(pady=20)
        return
    
    # === SECCIÓN DE INFORMACIÓN DEL PERFIL ===
    frm_info = tk.LabelFrame(parent_frame, text="Información del Perfil", padx=15, pady=15)
    frm_info.pack(padx=10, pady=10, fill=tk.X)
    
    # Nombre completo y username
    tk.Label(frm_info, text=f"Nombre: {usuario.get('nombre_completo', 'N/A')}", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
    tk.Label(frm_info, text=f"Usuario: @{username}", font=("Arial", 11)).pack(anchor="w", pady=2)
    
    # Saldo (solo visible si es mi perfil)
    if es_mi_perfil:
        saldo = usuario.get("saldo", 0.0)
        tk.Label(frm_info, text=f"Saldo: €{saldo:.2f}", font=("Arial", 11)).pack(anchor="w", pady=2)
    
    # Valoración media
    valoracion = usuario.get("valoracion_media", 0)
    val_texto = f"{valoracion:.1f}" if valoracion else "Sin valoraciones"
    tk.Label(frm_info, text=f"Valoración media: {val_texto} ⭐", font=("Arial", 11)).pack(anchor="w", pady=2)
    
    # === BOTONES DE ACCIÓN ===
    frm_acciones = tk.Frame(parent_frame, bg="white")
    frm_acciones.pack(pady=20, padx=10, fill=tk.X)
    
    # Botones principales
    frm_principales = tk.Frame(frm_acciones, bg="white")
    frm_principales.pack(fill=tk.X, pady=(0, 15))
    
    # Botón de ver productos del usuario (visible para todos)
    def on_ver_productos():
        from src.ui.productos.mis_productos_window import show_mis_productos_view
        show_mis_productos_view(parent_frame, username)
    
    tk.Button(
        frm_principales,
        text="📦 Ver Productos" if not es_mi_perfil else "📦 Mis Productos",
        command=on_ver_productos,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=20,
        pady=10
    ).pack(fill=tk.X, pady=5)
    
    # Los siguientes botones solo se muestran si es mi propio perfil
    if es_mi_perfil:
        def on_editar_perfil():
            from src.ui.perfil.editar_window import show_editar_perfil_view
            show_editar_perfil_view(parent_frame, username)
        
        tk.Button(
            frm_principales,
            text="✏️ Editar Perfil",
            command=on_editar_perfil,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        ).pack(fill=tk.X, pady=5)

        def on_gestionar_monedero():
            from src.ui.perfil.monedero_window import show_monedero_view
            show_monedero_view(parent_frame, username)
        
        tk.Button(
            frm_principales,
            text="💰 Gestionar Monedero",
            command=on_gestionar_monedero,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            padx=20,
            pady=10
        ).pack(fill=tk.X, pady=5)
        
        # Separador visual
        ttk.Separator(frm_acciones, orient="horizontal").pack(fill=tk.X, pady=10)
        
        # Botón de dar de baja (separado)
        def on_dar_baja():
            # Crear una pequeña ventana emergente para pedir la contraseña
            dialog = tk.Toplevel(parent_frame)
            dialog.title("Confirmar Baja")
            dialog.geometry("300x200")
            
            tk.Label(dialog, text="Introduce tu contraseña para confirmar:", wraplength=250).pack(pady=10)
            pass_var = tk.StringVar()
            entry = tk.Entry(dialog, textvariable=pass_var, show="*")
            entry.pack(pady=5)
            
            def ejecutar_baja():
                confirmacion = messagebox.askyesno("¡Atención!", "¿Estás seguro de que quieres eliminar tu cuenta? Esta acción no se puede deshacer.")
                if confirmacion:
                    try:
                        from src.services.perfiles.usuarios_service import dar_baja_usuario
                        from src.db.db_app import connect
                        from src.ui.login_window import show_login
                        
                        with connect() as cn:
                            dar_baja_usuario(cn, username, pass_var.get())
                        
                        messagebox.showinfo("Baja confirmada", "Tu cuenta ha sido eliminada. Gracias por usar Tikitun.")
                        dialog.destroy()
                        
                        # Redirección limpiando la raíz
                        root = parent_frame.winfo_toplevel()
                        for widget in root.winfo_children():
                            widget.destroy()
                        show_login(root)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            tk.Button(dialog, text="CONFIRMAR ELIMINACIÓN", bg="#F44336", fg="white", command=ejecutar_baja).pack(pady=20)

        tk.Button(
            frm_acciones,
            text="🗑️ Dar de Baja",
            command=on_dar_baja,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        ).pack(fill=tk.X, pady=5)
