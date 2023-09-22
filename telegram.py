#se ha creado un .py llamado config.py 
#donde se encuetra el TELEGRAM_TOKEN
#TELEGRAM_TOKEN = "-------------------"
from PIL import Image, ImageDraw, ImageFont
from config import TELEGRAM_TOKEN
import telebot
import requests
from geopy.geocoders import Nominatim 
import os #para borrar la imagen


bot = telebot.TeleBot(TELEGRAM_TOKEN) #interacion con tu bot

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.reply_to(message, "Bienvenido a el localizador del ISS dispones de los comandos llamados localizacion y dibujar con el primero sabes la ubicacion en tiempo real y con dibuajar para ver en un mapa donde se encuentra el ISS")

def water(lat, lon):
    if ((lat <= 45.158 and lat >= 30.543) and (lon >= -5.187 and lon <= 22.209)):
        return ("Mar Mediteraneo")
    elif ((lat <= 40.258 and lat >= 28.543) and (lon >= 22.209 and lon <= 35.209)):
        return ("Mar Mediteraneo")
    
    elif ((lat <= 47.158 and lat >= 41.543) and (lon <= 27.400 and lon >= 41.709)):
        return ("Mar Negro")
    
    elif ((lat <= 47.100 and lat >= 36.543) and (lon <= 47.400 and lon >= 55.709)):
        return ("Mar Caspio")
    
    elif ((lat <= 30.1478 and lat >= 21.669) and (lon >= -97.723 and lon <= -81.053)):
        return ("Golfo de México")
    elif ((lat <= 30.1478 and lat >= 18.408) and (lon >= -97.723 and lon <= -90.56)):
        return ("Golfo de México")
    
    elif ((lat >= -63 and lat <= 24.6) and (lon >= 35.46 and lon <= 136.8)):
        return ("Océano Índico")
    
    elif ((lat >= 8.612 and lat <= 22.488) and (lon <= -62.84 and lon >= -88.09)):
        return ("Mar Caribe")

    elif (lat <= 87.158 and lat >= 71.543):
        return ("Océano Ártico")

    elif ((lat <= -63 and lat >= -85.0543)):
        return ("Océano Antártico")

    elif ((lat <= 118.058 and lat >= -63) and (lon >= -69.400 and lon <= 24.709)):
        return ("Océano Atlántico")
    elif ((lat <= 71.543 and lat >= 19.048) and (lon <= 80.49 and lon >= -94.47)):
       return ("Océano Atlántico")

    elif ((lat <= 8.88 and lat >= -63) and (lon <= 27.400 and lon >= 41.709)):
        return ("Océano Pacífico")
    elif ((lat <= 8.88 and lat >= -63) and (lon >= -119.555 and lon <= -77.709)):
        return ("Océano Pacífico")
    elif ((lat < 71.543 and lat >= 0) and (lon >= -119.555 and lon <= 121.514)):
        return ("Océano Pacífico")
    
    return ("Nuestra base de datos no reconoce esta zona")

@bot.message_handler(commands=["localizacion"])
def bot_localizacion(message):
    response_iss = requests.get("http://api.open-notify.org/iss-now.json").json()
    lat_iss = float(response_iss["iss_position"]["latitude"])
    lon_iss = float(response_iss["iss_position"]["longitude"])

    geolocator = Nominatim(user_agent="https://www.google.es/maps/preview") 
    
    location = geolocator.reverse(f"{lat_iss}, {lon_iss}") 
    
    if (location == None):
        bot.reply_to(message, water(lat_iss,lon_iss))
    else:
        bot.reply_to(message, location.address)


@bot.message_handler(commands=["dibujar"])
def bot_draw(message):
    mapa = Image.open('world.png')
    draw = ImageDraw.Draw(mapa)

    archivo_a_borrar = "mapa.png"
    try:
        # Intenta borrar el archivo
        os.remove(archivo_a_borrar)
        print(f"El archivo {archivo_a_borrar} ha sido borrado con éxito.")
    except FileNotFoundError:
        print(f"El archivo {archivo_a_borrar} no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al intentar borrar el archivo: {str(e)}")

    response_iss = requests.get("http://api.open-notify.org/iss-now.json").json()
    lat_iss = float(response_iss["iss_position"]["latitude"])
    lon_iss = float(response_iss["iss_position"]["longitude"])
    longitud_min = -180
    latitud_max = 90
    longitud_max = 180
    latitud_min = -90
    pixel_x = int((lon_iss - longitud_min) * (720 / (longitud_max - longitud_min)))
    pixel_y = int((latitud_max - lat_iss) * (360 / (latitud_max - latitud_min)))

    radio = 4  # Tamaño del círculo en píxeles
    color = (255, 0, 0)  # Color rojo en formato RGB
    draw.ellipse((pixel_x - radio, pixel_y - radio, pixel_x + radio, pixel_y + radio), fill=color, outline=color)
    
    mapa.save('mapa.png')

    cid = message.chat.id
    bot.send_photo(cid, open('mapa.png', 'rb'))

# MAIN ###############################################
if __name__ == '__main__':
    print('Inicialiazando el bot')
    bot.infinity_polling()
    print('fin bucle')
