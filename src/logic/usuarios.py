# usuarios.py
# Procesamiento de usuarios, dashboard, búsqueda

import pandas as pd
from datetime import datetime
import logging
import os
import webbrowser
from .notificaciones import enviar_correo, enviar_whatsapp
from ..utils.helpers import cargar_credenciales

logging.basicConfig(filename='log_sistema.txt', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def procesar_usuarios():
    # ...existing code...
    # (Pega aquí la función procesar_usuarios del código original)
    # ...existing code...
    pass

def filas_tabla(lista, columnas):
    # ...existing code...
    # (Pega aquí la función filas_tabla del código original)
    # ...existing code...
    pass

def generar_dashboard(usuarios_vencidos, usuarios_7_dias, usuarios_1_dia, usuarios_0_dias, usuarios_nuevos, usuarios_notificados):
    # ...existing code...
    # (Pega aquí la función generar_dashboard del código original)
    # ...existing code...
    pass

def obtener_usuario_por_dni(dni):
    try:
        archivo = "usuario.xlsx"
        df = pd.read_excel(archivo)
        df.columns = df.columns.str.strip().str.lower()
        columna_dni = next((col for col in df.columns if "dni" in col), None)
        if not columna_dni:
            return None
        df[columna_dni] = df[columna_dni].apply(lambda x: str(int(x)).zfill(8) if pd.notna(x) else "")
        resultado = df[df[columna_dni] == dni]
        if not resultado.empty:
            fila = resultado.iloc[0]
            nombre = fila.get("apellidos y nombres", "")
            partes = nombre.split()
            apellido = partes[0] if len(partes) > 0 else ""
            return {
                "nombre": nombre,
                "apellido": apellido
            }
        return None
    except Exception:
        return None

