import tkinter as tk
from tkinter import messagebox


def show_favoritos_view(parent_frame, username="usuario_demo"):
    """
    Muestra la lista de productos favoritos del usuario en el frame principal.
    
    Funcionalidades futuras (RF3.2, RF3.3, RF3.4):
    - Consultar productos marcados como favoritos
    - Quitar productos de favoritos
    - Consultar detalles de cada producto
    - Filtrar/ordenar favoritos
    """
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Título
    tk.Label(
        parent_frame,
        text="♥ Mis Favoritos",
        font=("Arial", 16, "bold")
    ).pack(pady=20)
    
    # Información
    tk.Label(
        parent_frame,
        text="Aquí aparecerán los productos que hayas guardado como favoritos",
        font=("Arial", 10),
        fg="gray"
    ).pack(pady=5)
    
    # Frame scrollable para productos favoritos
    canvas = tk.Canvas(parent_frame, height=400)
    scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Productos favoritos de ejemplo (placeholder)
    favoritos_ejemplo = [
        {"titulo": "Bicicleta de montaña", "precio": "450.00", "vendedor": "maria_bikes"},
        {"titulo": "Smartphone Samsung", "precio": "199.99", "vendedor": "techstore"},
    ]
    
    if not favoritos_ejemplo:
        tk.Label(
            scrollable_frame,
            text="No tienes productos favoritos aún\n\n"
                 "Explora el Feed y marca productos con ♥",
            font=("Arial", 11),
            fg="gray",
            justify=tk.CENTER
        ).pack(pady=50)
    else:
        for i, prod in enumerate(favoritos_ejemplo):
            prod_frame = tk.Frame(scrollable_frame, relief=tk.RIDGE, borderwidth=2)
            prod_frame.pack(fill=tk.X, padx=20, pady=8)
            
            # Icono corazón
            tk.Label(
                prod_frame,
                text="♥",
                font=("Arial", 16),
                fg="red"
            ).pack(side=tk.LEFT, padx=10, pady=10)
            
            # Información del producto
            info_frame = tk.Frame(prod_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)
            
            tk.Label(
                info_frame,
                text=prod['titulo'],
                font=("Arial", 12, "bold")
            ).pack(anchor=tk.W)
            
            tk.Label(
                info_frame,
                text=f"€{prod['precio']} • por @{prod['vendedor']}",
                font=("Arial", 10),
                fg="gray"
            ).pack(anchor=tk.W)
            
            # Botones
            btn_frame = tk.Frame(prod_frame)
            btn_frame.pack(side=tk.RIGHT, padx=10)
            
            tk.Button(
                btn_frame,
                text="Ver producto",
                state=tk.DISABLED
            ).pack(side=tk.LEFT, padx=3)
            
            tk.Button(
                btn_frame,
                text="Quitar ♥",
                fg="red",
                state=tk.DISABLED
            ).pack(side=tk.LEFT, padx=3)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20))
