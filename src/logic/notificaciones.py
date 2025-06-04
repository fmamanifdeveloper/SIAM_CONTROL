# notificaciones.py
# Funciones de correo y WhatsApp

import logging
import smtplib
import time
import webbrowser
from email.message import EmailMessage

import pyautogui

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

def detectar_posicion_caja_texto(nombre_archivo="pos_caja_texto.json"):
    """
    Ventana para calibrar la posición X/Y del mouse para WhatsApp.
    """
    import json
    import tkinter as tk
    from tkinter import messagebox
    import threading

    def actualizar_posicion():
        while running[0]:
            x, y = pyautogui.position()
            label_xy.config(text=f"X: {x}    Y: {y}")
            root.update_idletasks()
            time.sleep(0.05)

    def guardar():
        try:
            x = entry_x.get().strip()
            y = entry_y.get().strip()
            if x == '' or y == '':
                messagebox.showerror("Error", "Debes ingresar ambos valores X e Y.")
                return
            x = int(x)
            y = int(y)
            with open(nombre_archivo, "w") as f:
                json.dump({'x': x, 'y': y}, f)
            messagebox.showinfo("Posición guardada", f"Posición guardada: x={x}, y={y}")
            running[0] = False
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Valor inválido: {e}")

    root = tk.Tk()
    root.title("Calibrar caja de texto")
    root.geometry("440x360")
    root.minsize(350, 260)
    root.resizable(True, True)
    label = tk.Label(root, text="Calibrar caja de texto", font=("Arial", 16, "bold"), justify="center")
    label.pack(pady=(22, 8))
    label_xy = tk.Label(root, text="X: -    Y: -", font=("Arial", 15))
    label_xy.pack(pady=(0, 18))
    frame = tk.Frame(root)
    frame.pack(pady=10)
    tk.Label(frame, text="X:", font=("Arial", 14)).grid(row=0, column=0, padx=14, pady=8)
    entry_x = tk.Entry(frame, font=("Arial", 14), width=10)
    entry_x.grid(row=0, column=1, padx=14, pady=8)
    tk.Label(frame, text="Y:", font=("Arial", 14)).grid(row=1, column=0, padx=14, pady=8)
    entry_y = tk.Entry(frame, font=("Arial", 14), width=10)
    entry_y.grid(row=1, column=1, padx=14, pady=8)
    btn_guardar = tk.Button(root, text="Guardar", font=("Arial", 15, "bold"), bg="#388E3C", fg="white", command=guardar)
    btn_guardar.pack(pady=22)
    running = [True]
    t = threading.Thread(target=actualizar_posicion, daemon=True)
    t.start()
    root.mainloop()

def cargar_posicion_caja_texto(nombre_archivo="pos_caja_texto.json"):
    import json
    try:
        with open(nombre_archivo, "r") as f:
            pos = json.load(f)
            return pos.get('x', 300), pos.get('y', 700)
    except Exception:
        return 300, 700

def enviar_whatsapp(telefono, mensaje, pos_caja_texto=None):
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
        if pos_caja_texto is None:
            pos_caja_texto = cargar_posicion_caja_texto()
        pyautogui.click(pos_caja_texto[0], pos_caja_texto[1])
        pyperclip.copy(mensaje)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        logging.info(f"Mensaje WhatsApp enviado a {telefono}")
        print(f"✅ Mensaje enviado a {telefono} usando WhatsApp Desktop.")
    except Exception as e:
        logging.error(f"Error al enviar mensaje por WhatsApp a {telefono}: {e}")
        print(f"⚠️ Error al enviar mensaje por WhatsApp: {e}")


