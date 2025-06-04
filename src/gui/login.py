# login.py
# Interfaz de login (Tkinter)

import tkinter as tk
from tkinter import messagebox
from src.utils.helpers import cargar_credenciales
from src.gui.buscar_dni import buscar_usuario_por_dni_ui


def login_ui():
    """
    Ventana principal de login. Si el login es exitoso, abre la ventana de búsqueda por DNI.
    """
    def verificar_credenciales():
        usuario = entrada_usuario.get().strip()
        contrasena = entrada_contrasena.get().strip()
        credenciales = cargar_credenciales()
        if usuario == credenciales.get("usuario") and contrasena == credenciales.get("contrasena"):
            messagebox.showinfo("Login", "Ingreso exitoso")
            ventana.withdraw()  # Oculta la ventana principal
            buscar_usuario_por_dni_ui(parent=ventana)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ventana = tk.Tk()
    ventana.title("Login - UTI")
    ventana.geometry("400x210")
    ventana.resizable(False, False)

    # Frame para centrar y dar padding al formulario
    frame = tk.Frame(ventana, padx=30, pady=30)
    frame.pack(expand=True)

    tk.Label(frame, text="Usuario:").grid(row=0, column=0, padx=10, pady=(10, 8), sticky="e")
    entrada_usuario = tk.Entry(frame)
    entrada_usuario.grid(row=0, column=1, padx=10, pady=(10, 8))

    tk.Label(frame, text="Contraseña:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    entrada_contrasena = tk.Entry(frame, show="*")
    entrada_contrasena.grid(row=1, column=1, padx=10, pady=8)

    # Permitir login con Enter en ambos campos
    entrada_usuario.bind('<Return>', lambda event: verificar_credenciales())
    entrada_contrasena.bind('<Return>', lambda event: verificar_credenciales())

    tk.Button(frame, text="Iniciar sesión", command=verificar_credenciales, width=15, bg="#1976D2", fg="white", activebackground="#1565C0", activeforeground="white").grid(row=2, column=0, columnspan=2, pady=(18, 8))
    entrada_usuario.focus_set()
    ventana.mainloop()

# Aquí debería ir el resto del código que se encargue de iniciar la aplicación,
# como por ejemplo una función main() que llame a login_ui().

