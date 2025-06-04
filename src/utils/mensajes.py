# mensajes.py
# Utilidades para construir mensajes y manejo de fechas
from datetime import date
import pandas as pd

def construir_cuerpo_bienvenida(nombre, codigo_personalizado):
    return (
        f"Hola, somos la Unidad de Tecnología de la Información (UTI).\n\n"
        f"Sr(a). {nombre}, ¡bienvenid@ al sistema SIAM SOFT!\n\n"
        f"Tus credenciales de acceso son:\n"
        f"Usuario: {codigo_personalizado}\n"
        f"Contraseña temporal: 123456\n\n"
        f"Por tu seguridad, te recomendamos cambiar la contraseña en tu primer ingreso.\n"
        f"Recuerda que el uso de la cuenta es PERSONAL e intransferible.\n\n"
        f"Para más información, visita nuestra página: https://www.muniyarabamba.gob.pe/\n"
    )

def construir_mensaje_whatsapp(nombre, fecha_fin, hoy, hora_actual):
    # Asegurar que fecha_fin y hoy sean objetos date, usando dayfirst=True para formato D-M-A
    if isinstance(fecha_fin, str):
        try:
            fecha_fin = pd.to_datetime(fecha_fin, errors='coerce', dayfirst=True).date()
        except Exception:
            return None
    if not isinstance(fecha_fin, date) or pd.isna(fecha_fin):
        return None
    if not isinstance(hoy, date):
        try:
            hoy = pd.to_datetime(hoy, errors='coerce', dayfirst=True).date()
        except Exception:
            return None
    dias_restantes = (fecha_fin - hoy).days
    if dias_restantes < 0:
        return f"Hola {nombre}, tu contrato ya venció. Comunícate con soporte para más información."
    elif dias_restantes == 7:
        return f"Hola {nombre}, soy el asistente virtual de Unidad Tecnologia de la Informacion(UTI) tu contrato vence en 7 días. ¡No olvides renovarlo para evitar el corte del sistema SIAM SOFT!"
    elif dias_restantes == 1:
        return f"Hola {nombre}, soy el asistente virtual de Unidad Tecnologia de la Informacion(UTI) te recordamos que tu contrato vence mañana. ¡Evita inconvenientes y renueva tu acceso al sistema SIAM SOFT lo antes posible!"
    elif dias_restantes == 0 and hora_actual < 17:
        return f"⚠️ Hola {nombre}, soy el asistente virtual de Unidad Tecnologia de la Informacion(UTI) tu acceso al sistema SIAM SOFT será suspendido hoy a las 5:00 PM. Si aún no has renovado tu vinculo laboral, Comunicate con soporte para mas informacion N° 989544883"
    return None

def obtener_codigo_personalizado(row, columns):
    col_apellidos = next((c for c in columns if 'apellidos' in c.lower()), None)
    col_dni = next((c for c in columns if 'dni' in c.lower()), None)
    apellido = row[columns.index(col_apellidos)] if col_apellidos else ''
    dni = str(row[columns.index(col_dni)]) if col_dni else ''
    primer_apellido = apellido.split()[0] if apellido else ''
    ultimos4_dni = dni[-4:] if len(dni) >= 4 else dni
    return f"{primer_apellido}{ultimos4_dni}"
