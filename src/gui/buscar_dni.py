import tkinter as tk
from tkinter import ttk
import pandas as pd
from src.logic.usuarios import obtener_usuario_por_dni
from src.logic.notificaciones import enviar_correo, enviar_whatsapp, detectar_posicion_caja_texto
import os
from tkinter import messagebox
from src.utils.mensajes import construir_cuerpo_bienvenida, construir_mensaje_whatsapp, obtener_codigo_personalizado

def buscar_usuario_por_dni_ui(parent=None):
    """
    Ventana con dos tablas: principal (Total de Usuarios) y Usuario Nuevos.
    Doble click en una fila migra el registro entre tablas. Botón Procesar Envios toma la data de ambas tablas.
    """
    try:
        df_global = pd.read_excel("usuario.xlsx")
        df_global.columns = [str(col) for col in df_global.columns]
        # Eliminar columna 'Act' si existe
        if 'Act' in df_global.columns:
            df_global = df_global.drop(columns=['Act'])
        # Eliminar columna 'Acciones' si existe
        if 'Acciones' in df_global.columns:
            df_global = df_global.drop(columns=['Acciones'])
        # Limpiar número celular
        col_cel = [col for col in df_global.columns if 'celular' in col.lower()]
        if col_cel:
            df_global[col_cel[0]] = df_global[col_cel[0]].astype(str).str.replace(r'[^0-9]', '', regex=True)
        # Formatear fecha vto
        col_fecha = [col for col in df_global.columns if 'vto' in col.lower() or 'venc' in col.lower()]
        if col_fecha:
            df_global[col_fecha[0]] = pd.to_datetime(df_global[col_fecha[0]], errors='coerce').dt.strftime('%d-%m-%Y')
    except Exception as e:
        df_global = None
        error_excel = str(e)

    ventana_dni = tk.Toplevel(parent) if parent else tk.Toplevel()
    ventana_dni.title("Buscar usuario por DNI")
    ventana_dni.geometry("1500x700")
    ventana_dni.resizable(True, True)

    def on_close():
        if parent:
            parent.destroy()
        ventana_dni.destroy()
    ventana_dni.protocol("WM_DELETE_WINDOW", on_close)

    # --- Filtros ---
    filtro_frame = tk.Frame(ventana_dni, padx=30, pady=10)
    filtro_frame.pack(anchor="nw")
    tk.Label(filtro_frame, text="Filtrar por DNI:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    filtro_dni = tk.Entry(filtro_frame)
    filtro_dni.grid(row=0, column=1, padx=5, pady=5)
    tk.Label(filtro_frame, text="Filtrar por Nombres y Apellidos:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    filtro_nombre = tk.Entry(filtro_frame)
    filtro_nombre.grid(row=0, column=3, padx=5, pady=5)

    # --- Tablas ---
    table_frame = tk.Frame(ventana_dni)
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Etiquetas de título
    label_total = tk.Label(table_frame, text="Total de Usuarios", font=("Arial", 14, "bold"))
    label_total.grid(row=0, column=0, sticky="w", pady=(0, 5))
    label_nuevos = tk.Label(table_frame, text="Usuarios Nuevos", font=("Arial", 14, "bold"))
    label_nuevos.grid(row=0, column=1, sticky="w", pady=(0, 5))

    # Columnas a mostrar (sin 'Acciones' ni 'Act')
    columns = [col for col in (list(df_global.columns) if df_global is not None else []) if col.lower() not in ['acciones', 'act']]
    tree_total = ttk.Treeview(table_frame, columns=columns, show="headings", height=15, selectmode="browse")
    for col in columns:
        tree_total.heading(col, text=col)
        # Ajustar el ancho de columnas específicas
        if 'apellidos' in col.lower() or 'nombres' in col.lower():
            tree_total.column(col, width=250, anchor="center")
        elif 'regimen' in col.lower():
            tree_total.column(col, width=200, anchor="center")
        elif 'tipo de contrato' in col.lower():
            tree_total.column(col, width=200, anchor="center")
        else:
            tree_total.column(col, width=120, anchor="center")
    tree_total.grid(row=1, column=0, sticky="nsew", padx=(0, 20))
    scroll_total = ttk.Scrollbar(table_frame, orient="vertical", command=tree_total.yview)
    tree_total.configure(yscroll=scroll_total.set)
    scroll_total.grid(row=1, column=0, sticky="nse")

    tree_nuevos = ttk.Treeview(table_frame, columns=columns, show="headings", height=15, selectmode="browse")
    for col in columns:
        tree_nuevos.heading(col, text=col)
        # Ajustar el ancho de columnas específicas
        if 'apellidos' in col.lower() or 'nombres' in col.lower():
            tree_nuevos.column(col, width=250, anchor="center")
        elif 'regimen' in col.lower():
            tree_nuevos.column(col, width=200, anchor="center")
        elif 'tipo de contrato' in col.lower():
            tree_nuevos.column(col, width=200, anchor="center")
        else:
            tree_nuevos.column(col, width=120, anchor="center")
    tree_nuevos.grid(row=1, column=1, sticky="nsew")
    scroll_nuevos = ttk.Scrollbar(table_frame, orient="vertical", command=tree_nuevos.yview)
    tree_nuevos.configure(yscroll=scroll_nuevos.set)
    scroll_nuevos.grid(row=1, column=1, sticky="nse")

    table_frame.grid_rowconfigure(1, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    table_frame.grid_columnconfigure(1, weight=1)

    if df_global is not None:
        for _, row in df_global.iterrows():
            tree_total.insert("", "end", values=list(row))
    else:
        tk.Label(table_frame, text=f"No se pudo cargar usuario.xlsx: {error_excel}", fg="red").grid(row=1, column=0)

    def filtrar_tabla(*args):
        dni_val = filtro_dni.get().strip()
        nombre_val = filtro_nombre.get().strip().lower()
        for item in tree_total.get_children():
            tree_total.delete(item)
        # Limpiar la tabla de Usuarios Nuevos al filtrar
        for item in tree_nuevos.get_children():
            tree_nuevos.delete(item)
        if df_global is not None:
            df_filtrado = df_global
            if dni_val:
                col_dni = [col for col in df_global.columns if 'dni' in col.lower()]
                if col_dni:
                    df_filtrado = df_filtrado[df_filtrado[col_dni[0]].astype(str).str.contains(dni_val, case=False, na=False)]
            if nombre_val:
                col_nom = [col for col in df_global.columns if 'apellidos' in col.lower() or 'nombres' in col.lower()]
                if col_nom:
                    df_filtrado = df_filtrado[df_filtrado[col_nom[0]].astype(str).str.lower().str.contains(nombre_val)]
            for _, row in df_filtrado.iterrows():
                tree_total.insert("", "end", values=list(row))
    filtro_dni.bind('<KeyRelease>', filtrar_tabla)
    filtro_nombre.bind('<KeyRelease>', filtrar_tabla)

    def mover_a_nuevos(event):
        item = tree_total.focus()
        if item:
            values = tree_total.item(item, 'values')
            tree_total.delete(item)
            tree_nuevos.insert("", "end", values=values)
    def mover_a_total(event):
        item = tree_nuevos.focus()
        if item:
            values = tree_nuevos.item(item, 'values')
            tree_nuevos.delete(item)
            tree_total.insert("", "end", values=values)
    tree_total.bind('<Double-1>', mover_a_nuevos)
    tree_nuevos.bind('<Double-1>', mover_a_total)

    def enviar_correos():
        data_nuevos = [tree_nuevos.item(i, 'values') for i in tree_nuevos.get_children()]
        col_email = next((c for c in columns if 'mail' in c.lower() or 'correo' in c.lower()), None)
        col_nombre = next((c for c in columns if 'nombre' in c.lower()), None)
        col_apellidos = next((c for c in columns if 'apellidos' in c.lower()), None)
        col_dni = next((c for c in columns if 'dni' in c.lower()), None)
        if not data_nuevos:
            messagebox.showinfo("Sin registros", "No hay usuarios nuevos para enviar correos.")
            return
        enviados_correo = 0
        for row in data_nuevos:
            if col_email and row[columns.index(col_email)]:
                try:
                    nombre = row[columns.index(col_nombre)] if col_nombre else ''
                    codigo_personalizado = obtener_codigo_personalizado(row, columns)
                    cuerpo = construir_cuerpo_bienvenida(nombre, codigo_personalizado)
                    enviar_correo(row[columns.index(col_email)], f"Bienvenido {nombre}", cuerpo)
                    enviados_correo += 1
                except Exception as e:
                    print(f"Error enviando correo: {e}")
        messagebox.showinfo("Envio de Correos", f"Correos enviados: {enviados_correo}")
        # Generar dashboard al finalizar
        try:
            from src.logic.usuarios import generar_dashboard, filas_tabla, render_dashboard_html
            dashboard = generar_dashboard([], [], [], [], data_nuevos, [])
            tablas_dict = {
                "TABLA_NUEVOS": filas_tabla(data_nuevos, columns)
            }
            ruta_html = render_dashboard_html(dashboard, tablas_dict)
            print(f"Dashboard generado en: {ruta_html}")
        except Exception as e:
            print(f"Error generando dashboard: {e}")

    def enviar_whatsapps():
        data_total = [tree_total.item(i, 'values') for i in tree_total.get_children()]
        col_cel = next((c for c in columns if 'celular' in c.lower() or 'telefono' in c.lower()), None)
        col_nombre = next((c for c in columns if 'nombre' in c.lower()), None)
        col_fecha = next((c for c in columns if 'vto' in c.lower() or 'venc' in c.lower()), None)
        if not data_total:
            messagebox.showinfo("Sin registros", "No hay usuarios en la tabla Total de Usuarios para enviar WhatsApp.")
            return
        enviados_whatsapp = 0
        from datetime import datetime
        import pandas as pd
        hoy = datetime.now().date()
        hora_actual = datetime.now().hour
        # Listas para dashboard
        usuarios_vencidos = []
        usuarios_7_dias = []
        usuarios_1_dia = []
        usuarios_0_dias = []
        for row in data_total:
            if col_cel and row[columns.index(col_cel)] and col_fecha and row[columns.index(col_fecha)]:
                try:
                    nombre = row[columns.index(col_nombre)] if col_nombre else ''
                    telefono = row[columns.index(col_cel)]
                    fecha_fin = pd.to_datetime(row[columns.index(col_fecha)], errors="coerce", dayfirst=True).date()
                    if pd.isna(fecha_fin):
                        continue
                    mensaje = construir_mensaje_whatsapp(nombre, fecha_fin, hoy, hora_actual)
                    dias_restantes = (fecha_fin - hoy).days if fecha_fin and hoy else None
                    if mensaje:
                        enviar_whatsapp(telefono, mensaje)
                        enviados_whatsapp += 1
                    # Clasificación para dashboard
                    if dias_restantes is not None:
                        if dias_restantes < 0:
                            usuarios_vencidos.append({"nombre": nombre, "telefono": telefono, "fecha_vencimiento": fecha_fin})
                        elif dias_restantes == 7:
                            usuarios_7_dias.append({"nombre": nombre, "telefono": telefono, "fecha_vencimiento": fecha_fin})
                        elif dias_restantes == 1:
                            usuarios_1_dia.append({"nombre": nombre, "telefono": telefono, "fecha_vencimiento": fecha_fin})
                        elif dias_restantes == 0 and hora_actual < 17:
                            usuarios_0_dias.append({"nombre": nombre, "telefono": telefono, "fecha_vencimiento": fecha_fin})
                except Exception as e:
                    print(f"Error enviando WhatsApp: {e}")
        messagebox.showinfo("Envio de WhatsApp", f"WhatsApp enviados: {enviados_whatsapp}")
        # Generar dashboard al finalizar
        try:
            from src.logic.usuarios import generar_dashboard, filas_tabla, render_dashboard_html
            dashboard = generar_dashboard(usuarios_vencidos, usuarios_7_dias, usuarios_1_dia, usuarios_0_dias, [], [])
            tablas_dict = {
                "TABLA_VENCIDOS": filas_tabla(usuarios_vencidos, ["nombre", "telefono", "fecha_vencimiento"]),
                "TABLA_7DIAS": filas_tabla(usuarios_7_dias, ["nombre", "telefono", "fecha_vencimiento"]),
                "TABLA_1DIA": filas_tabla(usuarios_1_dia, ["nombre", "telefono", "fecha_vencimiento"]),
                "TABLA_SUSPENDIDOS": filas_tabla(usuarios_0_dias, ["nombre", "telefono", "fecha_vencimiento"])
            }
            ruta_html = render_dashboard_html(dashboard, tablas_dict)
            print(f"Dashboard generado en: {ruta_html}")
        except Exception as e:
            print(f"Error generando dashboard: {e}")

    # --- Botones en una sola fila (tamaño normal/auto) ---
    botones_frame = tk.Frame(ventana_dni)
    botones_frame.pack(pady=15)

    btn_calibrar = tk.Button(
        botones_frame,
        text="Calibrar posición WhatsApp",
        bg="#388E3C",
        fg="white",
        font=("Arial", 10, "bold"),
        command=detectar_posicion_caja_texto
    )
    btn_calibrar.grid(row=0, column=0, padx=10)

    btn_envio_correos = tk.Button(
        botones_frame,
        text="Enviar Correos a Nuevos",
        bg="#1976D2",
        fg="white",
        font=("Arial", 12, "bold"),
        command=enviar_correos
    )
    btn_envio_correos.grid(row=0, column=1, padx=10)

    btn_envio_whatsapp = tk.Button(
        botones_frame,
        text="Enviar WhatsApp a Todos",
        bg="#43A047",
        fg="white",
        font=("Arial", 12, "bold"),
        command=enviar_whatsapps
    )
    btn_envio_whatsapp.grid(row=0, column=2, padx=10)

    # Al abrir la ventana, si no existe pos_caja_texto.json, forzar calibración
    if not os.path.exists("pos_caja_texto.json"):
        messagebox.showinfo("Calibración requerida", "Debes calibrar la posición de la caja de texto de WhatsApp antes de continuar.")
        detectar_posicion_caja_texto()
