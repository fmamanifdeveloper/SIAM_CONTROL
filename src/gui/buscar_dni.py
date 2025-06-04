import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from src.logic.usuarios import obtener_usuario_por_dni

def buscar_usuario_por_dni_ui(parent=None):
    """
    Ventana para buscar usuario por DNI y mostrar nombre y apellido si existe.
    Si parent es pasado, al cerrar la ventana de búsqueda se cierra la app.
    Incluye una tabla visual con la data del Excel y filtro por DNI.
    """
    # --- Cargar DataFrame global para la tabla ---
    try:
        df_global = pd.read_excel("usuario.xlsx")
        df_global.columns = [str(col) for col in df_global.columns]
    except Exception as e:
        df_global = None
        error_excel = str(e)

    def buscar():
        dni = entry_dni.get().strip()
        # --- Filtro tabla ---
        if df_global is not None:
            if dni:
                # Filtra por coincidencia exacta o parcial en cualquier columna
                mask = df_global.apply(lambda row: row.astype(str).str.contains(dni, case=False, na=False).any(), axis=1)
                df_filtrado = df_global[mask]
            else:
                df_filtrado = df_global
            actualizar_tabla(df_filtrado)
        # --- Filtro campos ---
        usuario = obtener_usuario_por_dni(dni)
        if usuario:
            entry_nombre.config(state="normal")
            entry_apellido.config(state="normal")
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, usuario.get('nombre', ''))
            entry_apellido.delete(0, tk.END)
            entry_apellido.insert(0, usuario.get('apellido', ''))
            entry_nombre.config(state="readonly")
            entry_apellido.config(state="readonly")
        else:
            entry_nombre.config(state="normal")
            entry_apellido.config(state="normal")
            entry_nombre.delete(0, tk.END)
            entry_apellido.delete(0, tk.END)
            entry_nombre.config(state="readonly")
            entry_apellido.config(state="readonly")
            if dni:
                messagebox.showinfo("Información", "Usuario no encontrado.")

    ventana_dni = tk.Toplevel(parent) if parent else tk.Toplevel()
    ventana_dni.title("Buscar usuario por DNI")
    ventana_dni.geometry("900x500")
    ventana_dni.resizable(True, True)

    def on_close():
        if parent:
            parent.destroy()
        ventana_dni.destroy()

    ventana_dni.protocol("WM_DELETE_WINDOW", on_close)

    frame = tk.Frame(ventana_dni, padx=30, pady=25)
    frame.pack(anchor="nw")
    tk.Label(frame, text="DNI:").grid(row=0, column=0, padx=10, pady=(10, 8), sticky="e")
    entry_dni = tk.Entry(frame)
    entry_dni.grid(row=0, column=1, padx=10, pady=(10, 8))
    entry_dni.bind('<Return>', lambda event: buscar())
    tk.Label(frame, text="Nombre:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    entry_nombre = tk.Entry(frame, state="readonly")
    entry_nombre.grid(row=1, column=1, padx=10, pady=8)
    tk.Label(frame, text="Apellido:").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    entry_apellido = tk.Entry(frame, state="readonly")
    entry_apellido.grid(row=2, column=1, padx=10, pady=8)
    tk.Button(frame, text="Buscar", command=buscar, width=15, bg="#1976D2", fg="white", activebackground="#1565C0", activeforeground="white").grid(row=3, column=0, columnspan=2, pady=(18, 8))
    entry_dni.focus_set()

    # --- Tabla visual con la data del Excel y scroll ---
    if df_global is not None:
        columns = list(df_global.columns)
        tree_frame = tk.Frame(ventana_dni)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side="right", fill="y")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, side="left")
        def actualizar_tabla(df):
            tree.delete(*tree.get_children())
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))
        actualizar_tabla(df_global)

        # Redefinir buscar para usar el closure de actualizar_tabla
        def buscar():
            dni = entry_dni.get().strip()
            # --- Filtro tabla ---
            if df_global is not None:
                if dni:
                    # Filtra por coincidencia exacta o parcial en cualquier columna
                    mask = df_global.apply(lambda row: row.astype(str).str.contains(dni, case=False, na=False).any(), axis=1)
                    df_filtrado = df_global[mask]
                else:
                    df_filtrado = df_global
                actualizar_tabla(df_filtrado)
            # --- Filtro campos ---
            usuario = obtener_usuario_por_dni(dni)
            if usuario:
                entry_nombre.config(state="normal")
                entry_apellido.config(state="normal")
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, usuario.get('nombre', ''))
                entry_apellido.delete(0, tk.END)
                entry_apellido.insert(0, usuario.get('apellido', ''))
                entry_nombre.config(state="readonly")
                entry_apellido.config(state="readonly")
            else:
                entry_nombre.config(state="normal")
                entry_apellido.config(state="normal")
                entry_nombre.delete(0, tk.END)
                entry_apellido.delete(0, tk.END)
                entry_nombre.config(state="readonly")
                entry_apellido.config(state="readonly")
                if dni:
                    messagebox.showinfo("Información", "Usuario no encontrado.")
        # Reasignar el comando del botón y el bind
        entry_dni.bind('<Return>', lambda event: buscar())
        btns = frame.grid_slaves(row=3, column=0)
        if btns:
            btns[0].config(command=buscar)
    else:
        tk.Label(ventana_dni, text=f"No se pudo cargar usuario.xlsx: {error_excel}", fg="red").pack()
