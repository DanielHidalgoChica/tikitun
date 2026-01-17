import tkinter as tk
from tkinter import messagebox
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.feed_busqueda_favs.favoritos_service import (
    consultar_favoritos,
    quitar_favorito
)

from src.ui.productos.detalle_window import show_detalle_view

from io import BytesIO

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def show_favoritos_view(parent_frame, username="bob"):
    """
    Muestra la lista de productos favoritos del usuario en el frame principal.

    Consulta en tiempo real los favoritos del usuario desde la BD y los renderiza.

    Funcionalidades (RF3.2, RF3.3, RF3.4):
    - Consultar productos marcados como favoritos ✓
    - Quitar productos de favoritos ✓
    - Mostrar solo productos disponibles ✓

    Args:
        parent_frame: Frame donde renderizar la vista
        username: Usuario autenticado
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
        text="Productos que has guardado como favoritos",
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

    # Obtener favoritos reales de la BD
    favoritos = []
    try:
        with connect() as cn:
            favoritos = consultar_favoritos(cn, username)
    except Exception as ex:
        messagebox.showerror("Error", f"No se pudieron cargar los favoritos: {str(ex)}")
        favoritos = []

    # Mostrar favoritos o mensaje vacío
    if not favoritos:
        tk.Label(
            scrollable_frame,
            text="No tienes productos favoritos aún\n\n"
                 "Explora el Feed y marca productos con ♥",
            font=("Arial", 11),
            fg="gray",
            justify=tk.CENTER
        ).pack(pady=50)
    else:
        for prod in favoritos:
            prod_frame = tk.Frame(scrollable_frame, relief=tk.RIDGE, borderwidth=2)
            prod_frame.pack(fill=tk.X, padx=20, pady=8)

            # Imagen del producto (si existe)
            imagen_data = prod.get('imagen')
            if imagen_data and PIL_AVAILABLE:
                try:
                    # Convertir bytes a imagen
                    image = Image.open(BytesIO(imagen_data))
                    # Redimensionar manteniendo aspecto (thumbnail pequeño)
                    image.thumbnail((80, 80))
                    photo = ImageTk.PhotoImage(image)

                    img_label = tk.Label(prod_frame, image=photo)
                    img_label.image = photo  # Mantener referencia
                    img_label.pack(side=tk.LEFT, padx=10, pady=5)
                except Exception:
                    # Si hay error con la imagen, mostrar placeholder
                    tk.Label(
                        prod_frame,
                        text="🖼️",
                        font=("Arial", 24),
                        fg="gray",
                        bg="#f0f0f0",
                        width=3,
                        height=2
                    ).pack(side=tk.LEFT, padx=10, pady=5)
            else:
                # Sin imagen o PIL no disponible
                tk.Label(
                    prod_frame,
                    text="🖼️",
                    font=("Arial", 24),
                    fg="gray",
                    bg="#f0f0f0",
                    width=3,
                    height=2
                ).pack(side=tk.LEFT, padx=10, pady=5)

            # Información del producto
            info_frame = tk.Frame(prod_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)

            tk.Label(
                info_frame,
                text=prod.get('titulo', 'Sin título'),
                font=("Arial", 12, "bold")
            ).pack(anchor=tk.W)

            precio = prod.get('precio', 0)
            vendedor = prod.get('username_vendedor', 'desconocido')
            tk.Label(
                info_frame,
                text=f"€{precio:.2f} • por @{vendedor}",
                font=("Arial", 10),
                fg="gray"
            ).pack(anchor=tk.W)

            # Botones
            btn_frame = tk.Frame(prod_frame)
            btn_frame.pack(side=tk.RIGHT, padx=10)

            tk.Button(
                btn_frame,
                text="Ver producto",
                command=lambda id_prod=prod['id_producto']: show_detalle_view(parent_frame, id_prod, username, origen="favoritos")
            ).pack(side=tk.LEFT, padx=3)

            # Botón Quitar con recarga automática
            def crear_quitar_handler(id_prod, user):
                """Factory para crear handler del botón Quitar."""
                def on_quitar():
                    cn = None
                    try:
                        cn = begin_transaction()
                        quitar_favorito(cn, user, id_prod)
                        commit(cn)
                        messagebox.showinfo("OK", "Producto eliminado de favoritos")
                        # Recarga automática: re-renderiza la vista
                        show_favoritos_view(parent_frame, user)
                    except Exception as ex:
                        if cn:
                            rollback(cn)
                        messagebox.showerror("Error", str(ex))
                return on_quitar

            tk.Button(
                btn_frame,
                text="Quitar ♥",
                fg="red",
                command=crear_quitar_handler(prod.get('id_producto'), username)
            ).pack(side=tk.LEFT, padx=3)

    # Empaquetar canvas y scrollbar
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20))
