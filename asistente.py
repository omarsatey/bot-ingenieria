import os
import telebot
from flask import Flask, request
from threading import Thread

# Creamos la mini app web para Render
app = Flask(__name__)
TOKEN = os.getenv('TELEGRAM_TOKEN', '8772412056:AAFsJ8Sf3IAEXxViyKLnHMDbcr7lE5eU6x0')
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "¡El bot está activo!"
@app.route(f'/{TOKEN}', methods=['POST', 'get'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    else:
        return "Error", 403

# Diccionario para guardar temporalmente los datos de cada cliente
usuarios = {}

@bot.message_handler(func=lambda m: True)
def gestionar_flujo(mensaje):
        chat_id = mensaje.chat.id
        if chat_id not in usuarios:
            usuarios[chat_id] = {'paso': 'nombre_telefono'}
            bot.reply_to(mensaje,
                         text="¡Hola! Bienvenido a **Ingeniería en sus manos**. 💻\nPara comenzar, por favor indíquenos su **nombre y número de teléfono**.")
            return

        paso = usuarios[chat_id]['paso']

        if paso == 'nombre_telefono':
            usuarios[chat_id]['nombre_telefono'] = mensaje.text
            usuarios[chat_id]['paso'] = 'necesidad'
            bot.reply_to(mensaje, text="¡Muchas gracias! ¿Qué **trabajo o proyecto** necesita realizar?")

        elif paso == 'necesidad':
            usuarios[chat_id]['necesidad'] = mensaje.text
            usuarios[chat_id]['paso'] = 'ubicacion_horario'
            bot.reply_to(mensaje,
                         text="Excelente. Por último, indíquenos su **ubicación** (dirección) y a qué **horario** prefiere que le hagamos la visita técnica.")

        elif paso == 'ubicacion_horario':
            usuarios[chat_id]['ubicacion_horario'] = mensaje.text
            usuarios[chat_id]['paso'] = 'adicional'  # <--- Asigna el siguiente paso
            bot.reply_to(mensaje,
                         text="Perfecto. ¿Necesita algún **otro trabajo o detalle adicional** para aprovechar la misma visita?")
        elif paso == 'adicional':
            usuarios[chat_id]['adicional'] = mensaje.text

            # Resumen final con los 3 pasos consolidados
            nombre_tel = usuarios[chat_id].get('nombre_telefono')
            necesidad = usuarios[chat_id].get('necesidad')
            adicional = usuarios[chat_id].get('adicional')
            ubicacion_horario = usuarios[chat_id].get('ubicacion_horario')

            resumen = f"**NUEVO CLIENTE:**\n- Contacto: {nombre_tel}\n- Proyecto/Trabajo: {necesidad}\n-Trabajo Adicional:{adicional}\n- Ubicación y Horario: {ubicacion_horario}"

            bot.reply_to(mensaje,
                         text="¡Muchas gracias! Hemos registrado sus datos correctamente.en un momento el ingeniero Omar Satey se cuminicara con usted.")
            bot.send_message(chat_id, resumen)
            bot.send_message(7598090125, f"NUEVA SOLICITUD:\n\n"+ resumen)
            usuarios.pop(chat_id)




