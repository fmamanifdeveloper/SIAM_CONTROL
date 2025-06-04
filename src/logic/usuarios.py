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
    """
    Genera filas HTML para una tabla a partir de una lista de diccionarios o tuplas y los nombres de columnas.
    """
    filas = []
    for item in lista:
        if isinstance(item, dict):
            fila = '<tr>' + ''.join(f'<td>{item.get(col, "")}</td>' for col in columnas) + '</tr>'
        elif isinstance(item, (list, tuple)):
            fila = '<tr>' + ''.join(f'<td>{str(val)}</td>' for val in item) + '</tr>'
        else:
            fila = f'<tr><td colspan="{len(columnas)}">{str(item)}</td></tr>'
        filas.append(fila)
    return '\n'.join(filas)

def generar_dashboard(usuarios_vencidos, usuarios_7_dias, usuarios_1_dia, usuarios_0_dias, usuarios_nuevos, usuarios_notificados):
    """
    Genera un resumen tipo dashboard de los usuarios según su estado de contrato y notificación.
    """
    dashboard = {
        "Total usuarios vencidos": len(usuarios_vencidos),
        "Total usuarios con 7 días": len(usuarios_7_dias),
        "Total usuarios con 1 día": len(usuarios_1_dia),
        "Total usuarios que vencen hoy": len(usuarios_0_dias),
        "Total usuarios nuevos": len(usuarios_nuevos),
        "Total usuarios notificados": len(usuarios_notificados),
    }
    # Puedes agregar más métricas si lo deseas
    return dashboard

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

def render_dashboard_html(dashboard, tablas_dict, template_path=None, output_dir=None):
    """
    Genera un archivo HTML de dashboard con los datos y tablas proporcionados.
    El archivo se guarda en output/dashboard-YYYYMMDD-HHMMSS.html
    """
    import os
    from datetime import datetime
    if template_path is None:
        template_path = os.path.join(os.path.dirname(__file__), '../gui/dashboard_template.html')
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), '../../output')
    os.makedirs(output_dir, exist_ok=True)
    with open(template_path, encoding='utf-8') as f:
        template = f.read()
    # Reemplazar los valores del dashboard
    html = template.replace('{{VENCIDOS}}', str(dashboard.get('Total usuarios vencidos', 0)))\
        .replace('{{FALTAN_7}}', str(dashboard.get('Total usuarios con 7 días', 0)))\
        .replace('{{FALTA_1}}', str(dashboard.get('Total usuarios con 1 día', 0)))\
        .replace('{{SUSPENDIDOS}}', str(dashboard.get('Total usuarios que vencen hoy', 0)))\
        .replace('{{NUEVOS}}', str(dashboard.get('Total usuarios nuevos', 0)))\
        .replace('{{NOTIFICADOS}}', str(dashboard.get('Total usuarios notificados', 0)))
    # Reemplazar las tablas
    for key, value in tablas_dict.items():
        if not value.strip() or 'No hay' in value or value.strip() == '<tr></tr>':
            html = html.replace('{{' + key + '}}', '')
        else:
            html = html.replace('{{' + key + '}}', value)
    # Nombre de archivo con fecha y hora
    now = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_path = os.path.join(output_dir, f'dashboard-{now}.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    # Abrir el dashboard en el navegador automáticamente
    import webbrowser
    webbrowser.open('file://' + os.path.abspath(output_path))
    return output_path

