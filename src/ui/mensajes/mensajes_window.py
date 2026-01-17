import tkinter as tk
from tkinter import messagebox
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.mensajes import mensajes_service

def render_mensajes(messages_frame, mensajes, mi_usuario):
    for widget in messages_frame.winfo_children():
        widget.destroy()

    for msg in mensajes:
        autor = msg['username']
        texto = msg['texto']
        fecha = msg['fecha']

        es_mio = autor == mi_usuario
        bg = "#DCF8C6" if es_mio else "#F1F0F0"
        anchor = tk.E if es_mio else tk.W
        justify = tk.RIGHT if es_mio else tk.LEFT

        # Burbuja
        bubble = tk.Frame(messages_frame, bg=bg, padx=8, pady=4)
        bubble.pack(anchor=anchor, pady=4, padx=10)

        tk.Label(bubble, text=autor, font=("Arial", 8, "bold"),
                 bg=bg, justify=justify).pack(anchor=anchor)

        tk.Label(bubble, text=texto, wraplength=300,
                 bg=bg, justify=justify).pack(anchor=anchor)

        tk.Label(bubble, text=str(fecha), font=("Arial", 7),
                 fg="gray", bg=bg).pack(anchor=anchor)


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
        for conv in conversaciones_inicio:
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
                text=conv['ultimo_mensaje'],
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
                        mensajes = mensajes_service.consultar_conversacion(cn, id_chat, user)
                        commit(cn)
                        print('guarda')
                        # Recarga automática: re-renderiza la vista
                        render_mensajes(messages_frame, mensajes, user)
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
    text="Mensajes",
    font=("Arial", 12, "bold")
    ).pack(pady=10)

    # Canvas + Scrollbar
    canvas = tk.Canvas(right_panel)
    scrollbar = tk.Scrollbar(right_panel, orient=tk.VERTICAL, command=canvas.yview)
    messages_frame = tk.Frame(canvas)

    messages_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=messages_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
   #  Área de escritura (abajo del panel derecho)
    bottom = tk.Frame(right_panel, pady=6)
    bottom.pack(fill=tk.X, side=tk.BOTTOM)

    btn_attach = tk.Button(bottom, text="📎", state=tk.DISABLED, width=3)
    btn_attach.pack(side=tk.LEFT, padx=6)

    entry_msg = tk.Entry(bottom)
    entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

    def enviar_mensaje():
        texto = entry_msg.get().strip()
        if not texto:
            return
        print("Enviar:", texto)
        entry_msg.delete(0, tk.END)

    btn_send = tk.Button(bottom, text="Enviar", width=8, command=enviar_mensaje)
    btn_send.pack(side=tk.RIGHT, padx=6)

    entry_msg.bind("<Return>", lambda e: enviar_mensaje())

    # Nota informativa
    tk.Label(
        parent_frame,
        text="💡 Funcionalidad en desarrollo:\n"
             "Podrás enviar/recibir mensajes relacionados con productos",
        font=("Arial", 9),
        fg="gray",
        justify=tk.CENTER
    ).pack(pady=10)
