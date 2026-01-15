import tkinter as tk
from tkinter import messagebox


def show_perfil_view(parent_frame, username="usuario_demo"):
    """
    Muestra la vista de gestión de perfil en el frame principal.
    
    Funcionalidades futuras:
    - Consultar información del perfil
    - Modificar datos personales (nombre, correo, ubicación, etc.)
    - Gestionar saldo del monedero (añadir/transferir)
    - Consultar productos publicados
    - Dar de baja la cuenta
    """
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Título
    tk.Label(
        parent_frame,
        text=f"👤 Perfil de {username}",
        font=("Arial", 16, "bold")
    ).pack(pady=20)
    
    # Placeholder de funcionalidades
    tk.Label(
        parent_frame,
        text="Aquí podrás gestionar tu perfil:\n\n"
             "• Ver y editar información personal\n"
             "• Gestionar saldo del monedero\n"
             "• Consultar tus productos publicados\n"
             "• Modificar preferencias\n"
             "• Dar de baja tu cuenta",
        justify=tk.LEFT,
        font=("Arial", 11)
    ).pack(pady=20)
    
    # Botones de demostración (sin funcionalidad)
    btn_frame = tk.Frame(parent_frame)
    btn_frame.pack(pady=20)
    
    tk.Button(
        btn_frame,
        text="Ver información",
        width=20,
        state=tk.DISABLED
    ).grid(row=0, column=0, padx=10, pady=5)
    
    tk.Button(
        btn_frame,
        text="Editar perfil",
        width=20,
        state=tk.DISABLED
    ).grid(row=0, column=1, padx=10, pady=5)
    
    tk.Button(
        btn_frame,
        text="Gestionar saldo",
        width=20,
        state=tk.DISABLED
    ).grid(row=1, column=0, padx=10, pady=5)
    
    tk.Button(
        btn_frame,
        text="Mis productos",
        width=20,
        state=tk.DISABLED
    ).grid(row=1, column=1, padx=10, pady=5)
