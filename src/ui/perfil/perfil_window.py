import tkinter as tk
from tkinter import messagebox, ttk
from src.db.db_app import connect
from src.repositories.perfiles import usuarios_repo
from src.repositories.productos import productos_repo


def show_perfil_view(parent_frame, username="bob"):
    """
    Muestra la vista de gestión de perfil (RF1.2).
    
    Consulta:
    - Información del perfil del usuario
    """
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Cargar datos del usuario
    try:
        with connect() as cn:
            usuario = usuarios_repo.get_usuario(cn, username)
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
    
    # Saldo
    saldo = usuario.get("saldo", 0.0)
    tk.Label(frm_info, text=f"Saldo: €{saldo:.2f}", font=("Arial", 11)).pack(anchor="w", pady=2)
    
    # Valoración media
    valoracion = usuario.get("valoracion_media", 0)
    val_texto = f"{valoracion:.1f}" if valoracion else "Sin valoraciones"
    tk.Label(frm_info, text=f"Valoración media: {val_texto} ⭐", font=("Arial", 11)).pack(anchor="w", pady=2)
    
    # === BOTONES DE ACCIÓN ===
    frm_acciones = tk.Frame(parent_frame, bg="white")
    frm_acciones.pack(pady=20, padx=10, fill=tk.X)
    
    def on_mis_productos():
        from src.ui.productos.mis_productos_window import show_mis_productos_view
        show_mis_productos_view(parent_frame, username)
    
    # Botones principales
    frm_principales = tk.Frame(frm_acciones, bg="white")
    frm_principales.pack(fill=tk.X, pady=(0, 15))
    
    tk.Button(
        frm_principales,
        text="📦 Mis Productos",
        command=on_mis_productos,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=20,
        pady=10
    ).pack(fill=tk.X, pady=5)
    
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
    tk.Button(
        frm_acciones,
        text="🗑️ Dar de Baja",
        state=tk.DISABLED,
        bg="#F44336",
        fg="white",
        font=("Arial", 10),
        padx=20,
        pady=10,
        disabledforeground="white"
    ).pack(fill=tk.X, pady=5)
