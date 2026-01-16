import tkinter as tk
from src.ui.productos.publicar_window import open_publicar_producto
from src.ui.perfil.perfil_window import show_perfil_view
from src.ui.feed.feed_window import show_feed_view
from src.ui.mensajes.mensajes_window import show_mensajes_view
from src.ui.favoritos.favoritos_window import show_favoritos_view
from src.db import db_app
import tkinter.messagebox as messagebox


def run_app(username="bob"):
    """
    Ventana principal de TikiTun con menú lateral y vista central.
    
    Args:
        username: Nombre de usuario autenticado (se pasará después del login)
    """
    root = tk.Tk()
    root.title("TikiTun")
    root.geometry("900x600")
    root.minsize(800, 500)
    
    # ===== HEADER =====
    header_frame = tk.Frame(root, bg="#4CAF50", height=50)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    tk.Label(
        header_frame,
        text="TikiTun",
        font=("Arial", 18, "bold"),
        bg="#4CAF50",
        fg="white"
    ).pack(side=tk.LEFT, padx=20, pady=10)
    
    tk.Label(
        header_frame,
        text=f"@{username}",
        font=("Arial", 11),
        bg="#4CAF50",
        fg="white"
    ).pack(side=tk.RIGHT, padx=20, pady=10)
    
    # ===== CONTENEDOR PRINCIPAL =====
    main_container = tk.Frame(root)
    main_container.pack(fill=tk.BOTH, expand=True)
    
    # ===== MENÚ LATERAL =====
    sidebar = tk.Frame(main_container, bg="#f0f0f0", width=150)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)
    
    # Variable para rastrear el botón activo
    active_button = {"current": None}
    
    def create_menu_button(parent, text, icon, command):
        """Crea un botón del menú lateral con estilo."""
        btn = tk.Button(
            parent,
            text=f"{icon}\n{text}",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#333",
            relief=tk.FLAT,
            width=12,
            height=3,
            cursor="hand2",
            command=lambda: on_menu_click(btn, command)
        )
        
        # Efectos hover
        def on_enter(e):
            if btn != active_button["current"]:
                btn.config(bg="#e0e0e0")
        
        def on_leave(e):
            if btn != active_button["current"]:
                btn.config(bg="#f0f0f0")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def on_menu_click(btn, command):
        """Maneja el click en un botón del menú."""
        # Restaurar estilo del botón anterior
        if active_button["current"]:
            active_button["current"].config(bg="#f0f0f0", fg="#333")
        
        # Aplicar estilo al botón activo
        btn.config(bg="#4CAF50", fg="white")
        active_button["current"] = btn
        
        # Ejecutar comando
        command()
    
    # Botones del menú
    btn_feed = create_menu_button(sidebar, "Feed", "📱", lambda: show_feed_view(content_frame, username))
    btn_feed.pack(pady=(20, 5), padx=10)
    
    btn_perfil = create_menu_button(sidebar, "Perfil", "👤", lambda: show_perfil_view(content_frame, username))
    btn_perfil.pack(pady=5, padx=10)
    
    btn_favoritos = create_menu_button(sidebar, "Favoritos", "♥", lambda: show_favoritos_view(content_frame, username))
    btn_favoritos.pack(pady=5, padx=10)
    
    btn_mensajes = create_menu_button(sidebar, "Mensajes", "📧", lambda: show_mensajes_view(content_frame, username))
    btn_mensajes.pack(pady=5, padx=10)
    
    btn_crear = create_menu_button(sidebar, "Crear", "+", lambda: open_publicar_producto(root))
    btn_crear.pack(pady=5, padx=10)
    
    # Developer button: abre diálogo para inicializar la BD
    def on_developer_init():
        """Muestra confirmación y llama a initialize_database (DROP + CREATE, sin datos)."""
        if not messagebox.askyesno(
            "Inicializar BD",
            "¿Deseas reinicializar la base de datos?\n\nEsto BORRARÁ todas las tablas existentes y las volverá a crear vacías."
        ):
            return

        try:
            # drop_first=True (default) + solo init.sql (default)
            result = db_app.initialize_database()
            dropped = len(result.get("dropped_tables", []))
            stmts = result["statements_executed"]
            message = f"Inicialización completada.\n\nTablas eliminadas: {dropped}\nSentencias ejecutadas: {stmts}"
            messagebox.showinfo("Éxito", message)
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Fichero SQL no encontrado: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar la BD: {e}")

    # Reemplazar caracteres de control por un emoji para que se muestre correctamente
    btn_dev = create_menu_button(sidebar, "Dev", "🛠", on_developer_init)
    btn_dev.pack(pady=20, padx=10)
    
    # ===== ÁREA DE CONTENIDO =====
    content_frame = tk.Frame(main_container, bg="white")
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Mostrar Feed por defecto
    show_feed_view(content_frame, username)
    btn_feed.config(bg="#4CAF50", fg="white")
    active_button["current"] = btn_feed
    
    root.mainloop()
