import tkinter as tk
from tkinter import messagebox
from src.services.perfiles import usuarios_service
from src.db.db_app import connect
from src.ui.theme import *
import re
import os
from PIL import Image, ImageTk


def show_login(parent=None) -> tuple[bool, str]:
    """Muestra ventana de login y opción crear cuenta. Devuelve (autenticado, username)."""
    # Si no se proporciona parent, crear una ventana raíz visible (no withdrawn)
    own_root = False
    if parent is None:
        root = tk.Tk()
        root.title("Iniciar sesión / Crear cuenta")
        root.geometry("450x700")
        root.resizable(False, False)
        own_root = True
    else:
        root = parent
        root.deiconify()

    result = {"ok": False, "username": ""}

    # Login frame
    frm_login = tk.LabelFrame(root, text="Iniciar sesión", padx=8, pady=8)
    frm_login.grid(row=0, column=0, padx=8, pady=8, sticky="ew")

    tk.Label(frm_login, text="Usuario:").grid(row=0, column=0, sticky="w")
    ent_user = tk.Entry(frm_login)
    ent_user.grid(row=0, column=1, pady=2)

    tk.Label(frm_login, text="Contraseña:").grid(row=1, column=0, sticky="w")
    ent_pass = tk.Entry(frm_login, show="*")
    ent_pass.grid(row=1, column=1, pady=2)

    def do_login():
        username = ent_user.get().strip()
        pwd = ent_pass.get()
        if not username:
            messagebox.showwarning("Error", "Introduzca usuario")
            return
        try:
            with connect() as cn:
                ok = usuarios_service.verificar_credenciales(cn, username, pwd)
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar: {e}")
            return
        if ok:
            result["ok"] = True
            result["username"] = username
            root.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    btn_login = tk.Button(frm_login, text="Iniciar sesión", width=20, command=do_login,
                          bg=PRIMARY_COLOR, fg="white", font=("Arial", 10, "bold"), 
                          relief=tk.RAISED, cursor="hand2")
    btn_login.grid(row=2, column=0, columnspan=2, pady=(6,0))

    # Create account frame
    frm_create = tk.LabelFrame(root, text="Crear cuenta", padx=8, pady=8)
    frm_create.grid(row=1, column=0, padx=8, pady=(0,8), sticky="ew")

    tk.Label(frm_create, text="Usuario:").grid(row=0, column=0, sticky="w")
    new_user = tk.Entry(frm_create)
    new_user.grid(row=0, column=1, pady=2)

    tk.Label(frm_create, text="Contraseña:").grid(row=1, column=0, sticky="w")
    new_pass = tk.Entry(frm_create, show="*")
    new_pass.grid(row=1, column=1, pady=2)

    tk.Label(frm_create, text="Nombre completo:").grid(row=2, column=0, sticky="w")
    new_name = tk.Entry(frm_create)
    new_name.grid(row=2, column=1, pady=2)
    
    tk.Label(frm_create, text="Correo electrónico:").grid(row=3, column=0, sticky="w")
    new_email = tk.Entry(frm_create)
    new_email.grid(row=3, column=1, pady=2)

    tk.Label(frm_create, text="Ubicación (lat, lon):").grid(row=4, column=0, sticky="w")
    new_lat = tk.Entry(frm_create, width=10)
    new_lat.grid(row=4, column=1, sticky="w", pady=2)
    new_lon = tk.Entry(frm_create, width=10)
    new_lon.grid(row=4, column=1, sticky="e", pady=2)

    tk.Label(frm_create, text="Rango (km):").grid(row=5, column=0, sticky="w")
    new_rango = tk.Entry(frm_create)
    new_rango.grid(row=5, column=1, pady=2)

    tk.Label(frm_create, text="Categorías de preferencia:").grid(row=6, column=0, sticky="w", pady=(8, 4))
    
    # Frame para los checkboxes de categorías
    frm_cats = tk.Frame(frm_create)
    frm_cats.grid(row=7, column=0, columnspan=2, sticky="w", padx=8, pady=4)
    
    # Obtener categorías disponibles de la BD
    categorias_disponibles = []
    try:
        with connect() as cn:
            categorias_disponibles = usuarios_service.get_categorias_disponibles(cn)

    except Exception as e:
        categorias_disponibles = []
    
    # Crear checkboxes para cada categoría
    cat_vars = {}
    for i, cat in enumerate(categorias_disponibles):
        var = tk.IntVar(value=0)
        chk = tk.Checkbutton(frm_cats, text=cat, variable=var)
        chk.grid(row=i // 2, column=i % 2, sticky="w", padx=4)
        cat_vars[cat] = var
    
    # Si no hay categorías, mostrar mensaje
    if not categorias_disponibles:
        tk.Label(frm_cats, text="(No hay categorías disponibles)", fg="red").grid(row=0, column=0, sticky="w", padx=4)

    mayoria_var = tk.IntVar(value=0)
    chk_mayoria = tk.Checkbutton(frm_create, text="Confirmo mayoría de edad", variable=mayoria_var)
    chk_mayoria.grid(row=9, column=0, columnspan=2, sticky="w")

    # Frame para el checkbox de política y el enlace
    frm_politica = tk.Frame(frm_create)
    frm_politica.grid(row=10, column=0, columnspan=2, sticky="w")
    
    polit_var = tk.IntVar(value=0)
    chk_polit = tk.Checkbutton(frm_politica, text="Acepto la ", variable=polit_var)
    chk_polit.pack(side=tk.LEFT)
    
    # Enlace clickeable a la política de privacidad
    def mostrar_politica_privacidad():
        """Abre una ventana con la política de privacidad."""
        import os
        ventana_politica = tk.Toplevel(root)
        ventana_politica.title("Política de Privacidad - TikiTun")
        ventana_politica.geometry("700x500")
        ventana_politica.resizable(True, True)
        
        # Frame con scrollbar
        frame_scroll = tk.Frame(ventana_politica)
        frame_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        texto = tk.Text(frame_scroll, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Courier", 10))
        texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=texto.yview)
        
        # Leer el archivo de política de privacidad
        ruta_politica = os.path.join(os.path.dirname(os.path.dirname(__file__)), "politica_privacidad.txt")
        try:
            with open(ruta_politica, "r", encoding="utf-8") as f:
                contenido = f.read()
            texto.insert(tk.END, contenido)
        except FileNotFoundError:
            texto.insert(tk.END, "Error: No se pudo encontrar el archivo de política de privacidad.")
        except Exception as e:
            texto.insert(tk.END, f"Error al cargar la política de privacidad: {e}")
        
        texto.config(state=tk.DISABLED)  # Solo lectura
        
        # Botón para cerrar
        tk.Button(ventana_politica, text="Cerrar", command=ventana_politica.destroy, 
                  bg=PRIMARY_COLOR, fg="white", padx=20, pady=5).pack(pady=10)
    
    lbl_enlace = tk.Label(frm_politica, text="política de privacidad", fg=PRIMARY_COLOR, cursor="hand2", font=("Arial", 9, "underline"))
    lbl_enlace.pack(side=tk.LEFT)
    lbl_enlace.bind("<Button-1>", lambda e: mostrar_politica_privacidad())
    
    tk.Label(frm_politica, text=" y condiciones").pack(side=tk.LEFT)

    def do_create():
        u = new_user.get().strip()
        p = new_pass.get()
        n = new_name.get().strip()
        email = new_email.get().strip()
        lat = new_lat.get().strip()
        lon = new_lon.get().strip()
        rango = new_rango.get().strip()
        mayoria = bool(mayoria_var.get())
        polit = bool(polit_var.get())
        
        # Obtener categorías seleccionadas
        cats_list = [cat for cat, var in cat_vars.items() if var.get()]

        if not (u and p and n and email and lat and lon and rango):
            messagebox.showwarning("Error", "Complete todos los campos obligatorios")
            return
        if not cats_list:
            messagebox.showwarning("Error", "Debe seleccionar al menos 1 categoría")
            return
        # basic validations
        if len(u) > 15:
            messagebox.showwarning("Error", "El nombre de usuario no puede tener más de 15 caracteres")
            return
        if not (8 <= len(p) <= 15):
            messagebox.showwarning("Error", "La contraseña debe tener entre 8 y 15 caracteres")
            return
        if " " in p:
            messagebox.showwarning("Error", "La contraseña no puede contener espacios")
            return
        if not re.search(r"[A-Z]", p) or not re.search(r"[a-z]", p) or not re.search(r"[0-9]", p) or not re.search(r"[^A-Za-z0-9]", p):
            messagebox.showwarning("Error", "La contraseña debe incluir mayúscula, minúscula, número y carácter especial")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Error", "Correo no tiene formato válido")
            return
        try:
            lat_f = float(lat); lon_f = float(lon)
        except Exception:
            messagebox.showwarning("Error", "Latitud/longitud no válidas")
            return
        try:
            rango_f = round(float(rango), 2)
            if rango_f < 0:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Error", "Rango no válido (número real positivo)")
            return
        if len(cats_list) > 6:
            messagebox.showwarning("Error", "Máximo 6 categorías permitidas")
            return

        usuario = {
            "username": u,
            "contraseña": p,
            "nombre_completo": n,
            "correo": email,
            "ubicacion": (lat_f, lon_f),
            "rango": rango_f,
            "categorias": cats_list,
            "mayoria_edad": mayoria,
            "aceptacion_politicas": polit,
            "saldo": 0.0,
            "cuenta_eliminada": False
        }
        try:
            # Abrir conexión y llamar al servicio que valida y persiste
            with connect() as cn:
                usuarios_service.dar_alta_usuario(cn, usuario)
            messagebox.showinfo("OK", "Cuenta creada. Inicie sesión.")
            ent_user.delete(0, tk.END); ent_user.insert(0, u)
            ent_pass.delete(0, tk.END); ent_pass.insert(0, p)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear cuenta: {e}")

    btn_create = tk.Button(frm_create, text="Crear cuenta", width=20, command=do_create,
                           bg=PRIMARY_COLOR, fg="white", font=("Arial", 10, "bold"),
                           relief=tk.RAISED, cursor="hand2")
    btn_create.grid(row=11, column=0, columnspan=2, pady=(6,0))

    # ===== LOGO (centrado) =====
    frm_logo = tk.Frame(root)
    frm_logo.grid(row=2, column=0, padx=8, pady=20)
    
    # Centrar el frame del logo en la ventana
    root.grid_columnconfigure(0, weight=1)
    
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "../../images/logo.png")
        if os.path.exists(logo_path):
            logo_img = Image.open(logo_path)
            logo_img.thumbnail((80, 80), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(frm_logo, image=logo_photo)
            logo_label.image = logo_photo  # Mantener referencia
            logo_label.pack()
        else:
            # Fallback a emoji si no existe
            tk.Label(frm_logo, text="🎵", font=("Arial", 40), fg=PRIMARY_COLOR).pack()
    except Exception:
        # Fallback a emoji si hay error
        tk.Label(frm_logo, text="🎵", font=("Arial", 40), fg=PRIMARY_COLOR).pack()

    # Handle window close event
    def on_close():
        result["ok"] = False
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Run mainloop only if we created the root window
    if own_root:
        root.mainloop()
    
    return result["ok"], result["username"]
