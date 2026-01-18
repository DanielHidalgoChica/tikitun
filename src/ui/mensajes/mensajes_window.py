import tkinter as tk
import io
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.mensajes import mensajes_service

def mostrar_resultados_busqueda(resultados):
    win = tk.Toplevel()
    win.title("Resultados de búsqueda")
    win.geometry("500x400")

    canvas = tk.Canvas(win)
    scrollbar = tk.Scrollbar(win, orient=tk.VERTICAL, command=canvas.yview)
    frame = tk.Frame(canvas)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for r in resultados:
        texto = f"[{r['fecha']}] @{r['username']} · {r['titulo']}\n{r['texto']}"
        tk.Label(frame, text=texto, wraplength=460, justify=tk.LEFT, anchor="w").pack(fill=tk.X, padx=8, pady=4)

def abrir_busqueda(username):
    win = tk.Toplevel()
    win.title("Buscar mensajes")
    win.geometry("420x320")

    tk.Label(win, text="Buscar en mensajes", font=("Arial", 12, "bold")).pack(pady=8)

    tk.Label(win, text="Usuario").pack(anchor="w", padx=10)
    entry_user = tk.Entry(win)
    entry_user.pack(fill=tk.X, padx=10)

    tk.Label(win, text="Texto contiene").pack(anchor="w", padx=10, pady=(8,0))
    entry_text = tk.Entry(win)
    entry_text.pack(fill=tk.X, padx=10)

    tk.Label(win, text="Fecha (YYYY-MM-DD)").pack(anchor="w", padx=10, pady=(8,0))
    entry_fecha = tk.Entry(win)
    entry_fecha.pack(fill=tk.X, padx=10)

     # ─── Toggle Archivados ──────────────────
    incluir_archivados = tk.BooleanVar(value=False)
    chk_arch = ttk.Checkbutton(
        win,
        text="Incluir chats archivados",
        variable=incluir_archivados
    )
    chk_arch.pack(anchor="w", padx=10, pady=8) 

    def ejecutar_busqueda():
        filtros = {
            "usuario": entry_user.get().strip(),
            "texto": entry_text.get().strip(),
            "fecha": entry_fecha.get().strip(),
            "incluir_archivados": incluir_archivados.get()
        }
        try:
            with connect() as cn:
                resultados = mensajes_service.buscar_mensajes(cn, username, filtros)
            mostrar_resultados_busqueda(resultados)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    tk.Button(win, text="Buscar", command=ejecutar_busqueda).pack(pady=12)

def render_mensajes(container, mensajes: list[dict], username_actual: str):
    # Limpiar mensajes anteriores
    for w in container.winfo_children():
        w.destroy()

    for msg in mensajes:
        es_mio = msg["username"] == username_actual

        # Frame contenedor por mensaje
        fila = tk.Frame(container)
        fila.pack(fill=tk.X, pady=2, padx=5)

        # Frame burbuja
        burbuja = tk.Frame(
            fila,
            bg="#DCF8C6" if es_mio else "#FFFFFF",
            padx=8,
            pady=5,
            relief=tk.RIDGE,
            borderwidth=1
        )

        # Texto del mensaje
        tk.Label(
            burbuja,
            text=msg["texto"],
            bg=burbuja["bg"],
            wraplength=280,
            justify=tk.LEFT
        ).pack(anchor=tk.W)

        if msg.get("adjunto"):
            img_data = msg["adjunto"]
            img = Image.open(io.BytesIO(img_data))
            img.thumbnail((220, 220))
            img_tk = ImageTk.PhotoImage(img)

            lbl_img = tk.Label(burbuja, image=img_tk, bg=burbuja["bg"])
            lbl_img.image = img_tk  
            lbl_img.pack(anchor="w", pady=4)

        # Pie con hora + leído
        estado = "✔✔" if msg.get("leido", 0) else "✔"
        pie = tk.Label(
            burbuja,
            text=f"{msg['fecha']}  {estado}",
            font=("Arial", 7),
            fg="gray",
            bg=burbuja["bg"]
        )
        pie.pack(anchor=tk.E)

        # Alineación izquierda/derecha
        if es_mio:
            burbuja.pack(side=tk.RIGHT, anchor=tk.E)
        else:
            burbuja.pack(side=tk.LEFT, anchor=tk.W)

def abrir_nuevo_chat(parent_frame, username):
    win = tk.Toplevel()
    win.title("Nuevo chat")
    win.geometry("300x180")

    tk.Label(win, text="Crear nueva conversación", font=("Arial", 11, "bold")).pack(pady=10)

    tk.Label(win, text="ID del producto").pack(anchor="w", padx=12)
    entry_id = tk.Entry(win)
    entry_id.pack(fill=tk.X, padx=12)

    def crear_chat():
        val = entry_id.get().strip()
        if not val.isdigit():
            messagebox.showerror("Error", "Introduce un ID de producto válido")
            return

        id_producto = int(val)

        try:
            cn = begin_transaction()
            creado = mensajes_service.crear_conversacion(cn, username, id_producto)
            commit(cn)
            if creado:
                messagebox.showinfo("OK", "Chat creado")
            else:
                messagebox.showinfo("Error", "Chat no creado")
            win.destroy()
            
            show_mensajes_view(parent_frame, username)  # recarga
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", str(ex))

    tk.Button(win, text="Crear", command=crear_chat).pack(pady=12)


def show_mensajes_view(parent_frame, username):
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
    
    tk.Button(
        parent_frame,
        text="🔍 Buscar mensajes",
        command=lambda: abrir_busqueda(username)
    ).pack(pady=5)

    btn_nuevo = tk.Button(parent_frame, text="➕ Nuevo chat", command=lambda: abrir_nuevo_chat(parent_frame, username))
    btn_nuevo.pack(side=tk.LEFT, padx=4)


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
    
    btn_hist = tk.Button(left_panel, text="📂 Ver histórico", command=lambda: show_historico_view(parent_frame, username))
    btn_hist.pack(pady=4)

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
                        messages_frame.current_chat_id = id_chat
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

    # Variable para guardar la imagen seleccionada
    imagen_bytes = {"data": None, "filename": ""}

    lbl_imagen = tk.Label(bottom, text="No seleccionada", fg="gray")
    lbl_imagen.pack(anchor="w", padx=6)

    def seleccionar_imagen():
        filepath = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png"), ("Todos", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, "rb") as f:
                imagen_bytes["data"] = f.read()
                imagen_bytes["filename"] = filepath.split("/")[-1]

            img = Image.open(filepath)
            img.thumbnail((120, 120))
            img_tk = ImageTk.PhotoImage(img)

            lbl_imagen.config(image=img_tk, text="")
            lbl_imagen.image = img_tk   

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la imagen: {e}")

    btn_attach = tk.Button(bottom, text="📎", width=3,  command=seleccionar_imagen)
    btn_attach.pack(side=tk.LEFT, padx=6)

    entry_msg = tk.Entry(bottom)
    entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

    def enviar_mensaje(user: str):
        texto = entry_msg.get().strip()
        if not texto and not imagen_bytes["data"]:
            return
        id_chat = getattr(messages_frame, "current_chat_id", None)
        if id_chat is None:
            messagebox.showwarning("Aviso", "No hay ninguna conversación abierta")
            return
        print("Enviar:", id_chat, user, texto)
        entry_msg.delete(0, tk.END)
        cn = None
        try:
            cn = begin_transaction()
            mensajes_service.enviar_mensaje(cn,{
                                    "id_chat": id_chat,
                                    "emisor": user,
                                    "texto": texto,
                                    "adjunto": imagen_bytes["data"]})
            commit(cn)
            mensajes = mensajes_service.consultar_conversacion(cn, id_chat, user)
            commit(cn)
            print('guarda')
            # Recarga automática: re-renderiza la vista
            # Reset UI
            entry_msg.delete(0, tk.END)
            lbl_imagen.config(image="", text="No seleccionada", fg="gray")
            imagen_bytes["data"] = None
            imagen_bytes["filename"] = ""
            render_mensajes(messages_frame, mensajes, user)
        except Exception as ex:
            if cn:
                rollback(cn)
            messagebox.showerror("Error", str(ex))

    btn_send = tk.Button(bottom, text="Enviar", width=8, command=lambda: enviar_mensaje(username))
    btn_send.pack(side=tk.RIGHT, padx=6)

    entry_msg.bind("<Return>", lambda e: enviar_mensaje(username))

def show_historico_view(parent_frame, username):
    """
    Muestra una vista de los chats archivados
    """
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Título
    tk.Label(
        parent_frame,
        text="📧 Archivo de Chats",
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
    
    btn_hist = tk.Button(left_panel, text="Volver", command=lambda: show_mensajes_view(parent_frame, username))
    btn_hist.pack(pady=4)

    conversaciones_inicio = []
    try:
        with connect() as cn:
            conversaciones_inicio = mensajes_service.listar_conversaciones_archivadas(cn, username)
    except Exception as ex:
        messagebox.showerror("Error", f"No se pudieron cargar las conversaciones: {str(ex)}")
        conversaciones_inicio = []

    if not conversaciones_inicio:
        tk.Label(
            left_panel,
            text="No tienes chats archivados",
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
                        messages_frame.current_chat_id = id_chat
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