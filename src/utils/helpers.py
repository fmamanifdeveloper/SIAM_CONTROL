# helpers.py
# Utilidades generales (leer credenciales, helpers)

import json
from tkinter import messagebox
import logging

def cargar_credenciales():
    """
    Carga credenciales desde un archivo JSON.
    """
    try:
        with open("credenciales.json", "r") as f:
            logging.info("Credenciales cargadas correctamente.")
            return json.load(f)
    except Exception as e:
        logging.error(f"No se pudo cargar credenciales: {e}")
        messagebox.showerror("Error", f"No se pudo cargar credenciales: {e}")
        return {}

