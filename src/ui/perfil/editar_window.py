"""
Vista de edición de perfil de usuario.
Implementa RF1.3: Modificar perfil de usuario.
"""
import tkinter as tk
from tkinter import messagebox, ttk
import re
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.repositories.perfiles import usuarios_repo


def show_editar_perfil_view(parent_frame, username: str):
    """Muestra la vista de edición de perfil del usuario.
    
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
        text="✏️ Editar Perfil",
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
            
            categorias_disponibles = usuarios_repo.get_categorias_disponibles(cn)
            categorias_preferidas = usuarios_repo.get_categorias_preferidas(cn, username)
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando datos: {e}")
        return
    
    # Contenedor con scroll
    canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # === SECCIÓN DE DATOS PERSONALES ===
    frm_datos = tk.LabelFrame(
        scrollable_frame,
        text="Datos Personales",
        padx=15,
        pady=15,
        bg="white"
    )
    frm_datos.pack(fill=tk.X, pady=10, padx=5)
    
    # Nombre completo
    tk.Label(frm_datos, text="Nombre Completo:", bg="white").pack(anchor="w", pady=(0, 5))
    nombre_var = tk.StringVar(value=usuario.get("nombre_completo", ""))
    tk.Entry(frm_datos, textvariable=nombre_var, width=40).pack(anchor="w", padx=10, pady=(0, 10))
    
    # Correo
    tk.Label(frm_datos, text="Correo Electrónico:", bg="white").pack(anchor="w", pady=(0, 5))
    correo_var = tk.StringVar(value=usuario.get("correo", ""))
    tk.Entry(frm_datos, textvariable=correo_var, width=40).pack(anchor="w", padx=10, pady=(0, 10))
    
    # === SECCIÓN DE UBICACIÓN ===
    frm_ubicacion = tk.LabelFrame(
        scrollable_frame,
        text="Ubicación",
        padx=15,
        pady=15,
        bg="white"
    )
    frm_ubicacion.pack(fill=tk.X, pady=10, padx=5)
    
    # Latitud
    frm_lat = tk.Frame(frm_ubicacion, bg="white")
    frm_lat.pack(fill=tk.X, pady=5)
    tk.Label(frm_lat, text="Latitud [-90,90]:", bg="white").pack(side=tk.LEFT, padx=(0, 10))
    lat_var = tk.StringVar(value=str(usuario.get("ubi_latitud", "")))
    tk.Entry(frm_lat, textvariable=lat_var, width=15).pack(side=tk.LEFT)
    
    # Longitud
    frm_lon = tk.Frame(frm_ubicacion, bg="white")
    frm_lon.pack(fill=tk.X, pady=5)
    tk.Label(frm_lon, text="Longitud [-180,180]:", bg="white").pack(side=tk.LEFT, padx=(0, 10))
    lon_var = tk.StringVar(value=str(usuario.get("ubi_longitud", "")))
    tk.Entry(frm_lon, textvariable=lon_var, width=15).pack(side=tk.LEFT)
    
    # === SECCIÓN DE RANGO ===
    frm_rango = tk.LabelFrame(
        scrollable_frame,
        text="Rango de Búsqueda",
        padx=15,
        pady=15,
        bg="white"
    )
    frm_rango.pack(fill=tk.X, pady=10, padx=5)
    
    tk.Label(frm_rango, text="Rango (km):", bg="white").pack(anchor="w", pady=(0, 5))
    rango_var = tk.StringVar(value=str(usuario.get("rango", "")))
    tk.Entry(frm_rango, textvariable=rango_var, width=15).pack(anchor="w", padx=10)
    
    # === SECCIÓN DE CATEGORÍAS PREFERIDAS ===
    frm_cats = tk.LabelFrame(
        scrollable_frame,
        text="Categorías Preferidas (entre 1 y 6)",
        padx=15,
        pady=15,
        bg="white"
    )
    frm_cats.pack(fill=tk.X, pady=10, padx=5)
    
    # Variables de checkboxes
    cat_vars = {}
    for cat in categorias_disponibles:
        var = tk.BooleanVar(value=cat in categorias_preferidas)
        cat_vars[cat] = var
        tk.Checkbutton(
            frm_cats,
            text=cat,
            variable=var,
            bg="white"
        ).pack(anchor="w", padx=10, pady=2)
    
    # === BOTONES DE ACCIÓN ===
    frm_botones = tk.Frame(scrollable_frame, bg="white")
    frm_botones.pack(fill=tk.X, pady=20, padx=5)
    
    def validar_y_guardar():
        """Valida y guarda los cambios del perfil."""
        # Validar nombre completo
        nombre = nombre_var.get().strip()
        
        # Validar correo
        correo = correo_var.get().strip()
        if correo and not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", correo):
            messagebox.showerror("Error", "Formato de correo inválido")
            return
        
        # Validar ubicación
        lat = lat_var.get().strip()
        lon = lon_var.get().strip()
        
        if lat or lon:
            if not lat or not lon:
                messagebox.showerror("Error", "Debes proporcionar ambas coordenadas (latitud y longitud) o ninguna")
                return
            try:
                lat = float(lat)
                lon = float(lon)
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    messagebox.showerror("Error", "Coordenadas fuera de rango")
                    return
            except ValueError:
                messagebox.showerror("Error", "Latitud y longitud deben ser números")
                return
        
        # Validar rango
        rango = rango_var.get().strip()
        if rango:
            try:
                rango = float(rango)
                if rango <= 0:
                    messagebox.showerror("Error", "El rango debe ser mayor a 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "El rango debe ser un número")
                return
        
        # Validar categorías
        categorias_seleccionadas = [cat for cat, var in cat_vars.items() if var.get()]
        if not categorias_seleccionadas:
            messagebox.showerror("Error", "Debes seleccionar al menos una categoría preferida")
            return
        if len(categorias_seleccionadas) > 6:
            messagebox.showerror("Error", "Máximo 6 categorías permitidas")
            return
        
        # Guardar cambios
        cn = begin_transaction()
        try:
            # Preparar cambios
            cambios = {}
            if nombre:
                cambios["nombre_completo"] = nombre
            if correo and correo != usuario.get("correo"):
                # Verificar unicidad de correo
                cur = cn.cursor()
                cur.execute(
                    "SELECT username FROM Usuario WHERE correo = ? AND username != ?",
                    (correo, username)
                )
                if cur.fetchone():
                    messagebox.showerror("Error", "Este correo ya está en uso")
                    rollback(cn)
                    return
                cur.close()
                cambios["correo"] = correo
            
            if lat is not None and lon is not None:
                cambios["ubi_latitud"] = lat
                cambios["ubi_longitud"] = lon
            elif not lat and not lon:
                cambios["ubi_latitud"] = None
                cambios["ubi_longitud"] = None
            
            if rango:
                cambios["rango"] = rango
            
            # Actualizar usuario
            if cambios:
                usuarios_repo.update_usuario(cn, username, cambios)
            
            # Actualizar categorías preferidas
            usuarios_repo.update_categorias_preferidas(cn, username, categorias_seleccionadas)
            
            commit(cn)
            messagebox.showinfo("Éxito", "Perfil actualizado correctamente")
            
            # Volver a la vista de perfil
            from src.ui.perfil.perfil_window import show_perfil_view
            show_perfil_view(parent_frame, username)
            
        except ValueError as e:
            rollback(cn)
            messagebox.showerror("Error", str(e))
        except Exception as e:
            rollback(cn)
            messagebox.showerror("Error", f"Error guardando cambios: {e}")
    
    def volver():
        """Vuelve a la vista de perfil sin guardar."""
        from src.ui.perfil.perfil_window import show_perfil_view
        show_perfil_view(parent_frame, username)
    
    tk.Button(
        frm_botones,
        text="💾 Guardar Cambios",
        command=validar_y_guardar,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=20,
        pady=10
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        frm_botones,
        text="❌ Cancelar",
        command=volver,
        bg="#F44336",
        fg="white",
        font=("Arial", 10),
        padx=20,
        pady=10
    ).pack(side=tk.LEFT, padx=5)
