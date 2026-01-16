import tkinter as tk
from tkinter import messagebox


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
        {"usuario": "maria_bikes", "producto": "Bicicleta de montaña", "ultimo_msg": "¿Sigue disponible?"},
        {"usuario": "juan123", "producto": "Guitarra eléctrica", "ultimo_msg": "Te la dejo en 250€"},
    ]
    
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
