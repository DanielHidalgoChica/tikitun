import tkinter as tk
from tkinter import messagebox


def show_feed_view(parent_frame, username="bob"):
    """
    Muestra el feed de recomendaciones en el frame principal.
    
    Funcionalidades futuras (RF3.1, RF3.5):
    - Mostrar productos recomendados según preferencias del usuario
    - Filtrar por categorías preferidas
    - Ordenar por grado de promoción y puntuación del vendedor
    - Barra de búsqueda de productos (fuzzy search)
    - Filtros por categoría y precio
    - Consultar detalles de cada producto
    """
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Título
    tk.Label(
        parent_frame,
        text="📱 Feed de Recomendaciones",
        font=("Arial", 16, "bold")
    ).pack(pady=10)
    
    # Barra de búsqueda
    search_frame = tk.Frame(parent_frame)
    search_frame.pack(pady=10, padx=20, fill=tk.X)
    
    tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    search_entry = tk.Entry(search_frame, width=40)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        search_frame,
        text="Buscar",
        state=tk.DISABLED
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        search_frame,
        text="Filtros ▼",
        state=tk.DISABLED
    ).pack(side=tk.LEFT, padx=5)
    
    # Separador
    tk.Frame(parent_frame, height=2, bg="gray").pack(fill=tk.X, pady=10)
    
    # Lista de productos recomendados (placeholder)
    tk.Label(
        parent_frame,
        text="Productos recomendados para ti:",
        font=("Arial", 12, "bold")
    ).pack(pady=10)
    
    # Frame scrollable para productos
    canvas = tk.Canvas(parent_frame, height=400)
    scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Productos de ejemplo (placeholder)
    productos_ejemplo = [
        {"titulo": "Guitarra eléctrica", "precio": "299.99", "vendedor": "juan123"},
        {"titulo": "Bicicleta de montaña", "precio": "450.00", "vendedor": "maria_bikes"},
        {"titulo": "Smartphone Samsung", "precio": "199.99", "vendedor": "techstore"},
    ]
    
    for i, prod in enumerate(productos_ejemplo):
        prod_frame = tk.Frame(scrollable_frame, relief=tk.RIDGE, borderwidth=2)
        prod_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            prod_frame,
            text=f"📦 {prod['titulo']}",
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(
            prod_frame,
            text=f"€{prod['precio']}",
            font=("Arial", 11),
            fg="green"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            prod_frame,
            text=f"por @{prod['vendedor']}",
            font=("Arial", 9),
            fg="gray"
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            prod_frame,
            text="Ver más",
            state=tk.DISABLED
        ).pack(side=tk.RIGHT, padx=10, pady=5)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
