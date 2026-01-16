import tkinter as tk
from tkinter import messagebox
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.mensajes import mensajes_service

def show_mensajes_view(parent_frame, username="bob"):
    """
    Muestra la vista de gestión de mensajes en el frame principal.
    
    Funcionalidades futuras (RF5.1 - RF5.5):
    - Listar conversaciones abiertas
    - Consultar mensajes de una conversación
    - Enviar mensajes a otros usuarios
    - Adjuntar archivos
    - Buscar mensajes
    - Marcar mensajes como leídos
    - Archivar conversaciones finalizadas
    """
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Título
    tk.Label(
        parent_frame,
        text="📧 Mensajes",
        font=("Arial", 16, "bold")
    ).pack(pady=20)
    
    # Contenedor principal dividido en dos
    main_container = tk.Frame(parent_frame)
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # Panel izquierdo: Lista de conversaciones
    left_panel = tk.Frame(main_container, relief=tk.RIDGE, borderwidth=2)
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
    
    tk.Label(
        left_panel,
        text="Conversaciones",
        font=("Arial", 12, "bold")
    ).pack(pady=10)
    
    # Lista de conversaciones (placeholder)
 
    conversaciones_ejemplo = [
        {"id_chat": "1", "usuario": "maria_bikes", "producto": "Bicicleta de montaña", "ultimo_msg": "¿Sigue disponible?"},
        {"id_chat": "2","usuario": "juan123", "producto": "Guitarra eléctrica", "ultimo_msg": "Te la dejo en 250€"},
    ]
    
    conversaciones_inicio = []
    try:
        with connect() as cn:
            conversaciones_inicio = mensajes_service.listar_conversaciones_inicio(cn, username)
    except Exception as ex:
        messagebox.showerror("Error", f"No se pudieron cargar las conversaciones: {str(ex)}")
        conversaciones_inicio = []

    if not conversaciones_inicio:
        tk.Label(
            left_panel,
            text="No tienes chats iniciados",
            font=("Arial", 11),
            fg="gray",
        ).pack(expand=True)

    else:
        for conv in conversaciones_ejemplo:
            conv_frame = tk.Frame(left_panel, relief=tk.RAISED, borderwidth=1)
            conv_frame.pack(fill=tk.X, padx=5, pady=3)
            
            tk.Label(
                conv_frame,
                text=f"@{conv['usuario']}",
                font=("Arial", 10, "bold")
            ).pack(anchor=tk.W, padx=5, pady=2)
            
            tk.Label(
                conv_frame,
                text=f"Re: {conv['producto']}",
                font=("Arial", 9),
                fg="gray"
            ).pack(anchor=tk.W, padx=5)
            
            tk.Label(
                conv_frame,
                text=conv['ultimo_msg'],
                font=("Arial", 9)
            ).pack(anchor=tk.W, padx=5, pady=2)

            # Botones
            btn_frame = tk.Frame(conv_frame)
            btn_frame.pack(side=tk.RIGHT, padx=10)

            # Botón Seleccionar con recarga automática
            def seleccionar_chat(id_chat, user):
                """Factory para crear handler del botón Seleccionar."""
                def on_seleccionar():
                    cn = None
                    try:
                        cn = begin_transaction()
                        mensajes_service.consultar_conversacion(cn, user, id_chat)
                        commit(cn)
                        messagebox.showinfo("OK", "Seleccionado")
                        # Recarga automática: re-renderiza la vista
                        show_mensajes_view(parent_frame, user)
                    except Exception as ex:
                        if cn:
                            rollback(cn)
                        messagebox.showerror("Error", str(ex))
                return on_seleccionar
            
            tk.Button(
                btn_frame,
                text="Abrir",
                fg="black",
                command=seleccionar_chat(conv.get('id_chat'), username)
            ).pack(side=tk.LEFT, padx=3)
            
        
    # Panel derecho: Mensajes de la conversación seleccionada
    right_panel = tk.Frame(main_container, relief=tk.RIDGE, borderwidth=2)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
    
    tk.Label(
        right_panel,
        text="Selecciona una conversación",
        font=("Arial", 11),
        fg="gray"
    ).pack(expand=True)
    
    # Nota informativa
    tk.Label(
        parent_frame,
        text="💡 Funcionalidad en desarrollo:\n"
             "Podrás enviar/recibir mensajes relacionados con productos",
        font=("Arial", 9),
        fg="gray",
        justify=tk.CENTER
    ).pack(pady=10)
