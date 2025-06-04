# notificaciones.py
# Funciones de correo y WhatsApp

from email.message import EmailMessage
import smtplib
import webbrowser
import time
import pyautogui
import logging

# --- UTILIDADES DE NOTIFICACIÓN ---
def enviar_correo(destinatario, asunto, cuerpo):
    """
    Envía un correo electrónico usando SMTP SSL (Gmail).
    """
    try:
        remitente = "informaticauti9@gmail.com"
        contraseña = "ybnl zlka qwgb phrs"
        msg = EmailMessage()
        msg.set_content(cuerpo)
        msg["Subject"] = asunto
        msg["From"] = remitente
        msg["To"] = destinatario
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, contraseña)
            smtp.send_message(msg)
        logging.info(f"Correo enviado a {destinatario} con asunto '{asunto}'")
    except Exception as e:
        logging.error(f"Error al enviar correo a {destinatario}: {e}")
        raise

def enviar_whatsapp(telefono, mensaje):
    """
    Envía un mensaje por WhatsApp Desktop automatizando el proceso.
    """
    try:
        if not telefono.startswith("+"):
            telefono = "+51" + telefono
        webbrowser.open(f"whatsapp://send?phone={telefono}")
        time.sleep(7)
        import pyperclip
        import pygetwindow as gw
        ventana = None
        for w in gw.getAllWindows():
            if w.title and "WhatsApp" in w.title:
                ventana = w
                break
        if ventana:
            try:
                ventana.activate()
                ventana.maximize()
            except Exception as e:
                logging.warning(f"No se pudo maximizar/activar ventana WhatsApp: {e}")
        else:
            logging.error("No se encontró ventana de WhatsApp para activar.")
            print("No se encontró ventana de WhatsApp para activar.")
            return
        pyautogui.click(300, 700)
        pyperclip.copy(mensaje)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        logging.info(f"Mensaje WhatsApp enviado a {telefono}")
        print(f"✅ Mensaje enviado a {telefono} usando WhatsApp Desktop.")
    except Exception as e:
        logging.error(f"Error al enviar mensaje por WhatsApp a {telefono}: {e}")
        print(f"⚠️ Error al enviar mensaje por WhatsApp: {e}")

