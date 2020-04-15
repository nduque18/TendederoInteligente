# Implementacion de los sockets para la WEB #
try:
  import usocket as socket
except:
  import socket
# Librerias a utilizar #
import time
import os
import utime
import sys
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from machine import Pin, PWM
esp.osdebug(None)
import gc
gc.collect()
last_measurement_time = 0
# Datos de la red Wi-Fi local #
ssid = 'Opportunity'
password = 'BenjiBw07'
# Configuración de la conexión Wi-Fi #
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
# Conexión a la red Wi-Fi #
while station.isconnected() == False:
  pass
print('Conexion exitosa con la red %s' % ssid)
print('Direccion IP local, mascara, puerta de enlace, DNS primario')
print(station.ifconfig())
# Creacion de la identificación del cliente #
myIDnum = int.from_bytes(os.urandom(3), 'little')
myMQTT = bytes("client_"+str(myIDnum), 'utf-8')
# Credenciales de Thinkspeak #
THINGSPEAK_URL = b"mqtt.thingspeak.com" 
THINGSPEAK_USER_ID = b'YLLE2FI1ZXFJQVD6'
THINGSPEAK_MQTT_API_KEY = b'GEZ3FMKWWSDQFQLU'
# Asignación de credenciales e información del cliente a la función client del UMQTTsimple #
client = MQTTClient(client_id = myMQTT, server = THINGSPEAK_URL, user = THINGSPEAK_USER_ID, password = THINGSPEAK_MQTT_API_KEY, ssl = False) 
# Creacion de variables y asignación a pines #
Lluvia = Pin(16, Pin.IN)
led = Pin(2, Pin.OUT)
servo = PWM(Pin(14), freq=50, duty=30)
estado = 0
# Función de la página Web #
def web_page(estado):
# Asignación de la vaiable clima y estado del techo para mostrar #    
  if Lluvia.value() == 1:
    Clima="No hay lluvia."
  else:
    Clima="Hay lluvia."
  if estado == 0:
    Es= "Cerrado"
  else:
    Es= "Abierto" 
# HTML de la página Web # 
  html = """<html><head><title>Detector de Lluvia &#127783;</title><meta name="viewport"content="width=device-width, initial-scale=1"><META HTTP-EQUIV="REFRESH" CONTENT="10;URL=/"> </head><link rel="icon" href="data:,"><link rel="icon" href="data:,"> <style> html{font-family: Helvetica; display:inline-block; margin: 10px auto; text-align: center;}h1{color: #0F3375; padding: 5vh;}p{font-size: 1.8rem;}.button{display: inline-block; background-color: #008F39; border: none;border-radius: 4px; color: white; padding: 16px 30px; text-decoration: none; font-size: 40px; margin: 2px; cursor: pointer;}.button2{background-color: #cc0000;}
        </style></head><body><h1>Detector de Lluvia &#127783;</h1><p>Estado del clima:<strong>""" + Clima + """ </strong> Estado del techo: <strong> """ + Es + """ </strong></p><p><strong> Que desea hacer? </strong></p><p><a href="/?cerrar=no"><button class="button">ABRIR </button> </a></p>
        <p><a href="/?cerrar=yes"><button class="button button2">CERRAR</button></body>
</html>"""
  return html
# Configuración de los Sockets TCP #
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.0.254', 80))
s.listen(5)
# Credenciales para publicar en Thinkspeak #
THINGSPEAK_CHANNEL_ID = b'1022434'
THINGSPEAK_CHANNEL_WRITE_API_KEY = b'ANZ6JAHJLQ7C40SU'
PUBLISH_PERIOD_IN_SEC = 1
while True:
    current_time = time.time()
    #Enviar datos cada 15 segundos #
    if current_time - last_measurement_time > 15:
        # Envio de los datos a Thinkgspeak #
        Valorlluvia = not Lluvia.value()
        credentials = bytes("channels/{:s}/publish/{:s}".format(THINGSPEAK_CHANNEL_ID, THINGSPEAK_CHANNEL_WRITE_API_KEY), 'utf-8')
        last_measurement_time = current_time
        payload = bytes("field1={:.1f}\n".format(Valorlluvia), 'utf-8')
        client.connect()
        print('Envio de datos a Thinkspeak')
        client.publish(credentials, payload)
        client.disconnect() 
        time.sleep(PUBLISH_PERIOD_IN_SEC)
    # Interacción con la página Web #
    conn, addr = s.accept()
    print('Conexion desde %s' % str(addr))
    request = conn.recv(4097)
    request = str(request)
    typecont = str(request)
    print('Contenido = %s' % request)
    led_on = request.find('/?cerrar=yes')
    led_off = request.find('/?cerrar=no')
    detection = typecont.find ('/?cerrar=yes')
    #print( 'Esto es deteccion', detection)
    # Manejo del actuador #
    if led_on == 6 or detection == 138:
      print('Cerrar')
      led.value(1)
      estado = 0
      servo.duty(30)
    if led_off == 6:
      print('Abrir')
      led.value(0)
      estado = 1
      servo.duty(122)
    # Finalizacion de la conexion Web # Esta se reinicia automaticamente en el HTML 
    response = web_page(estado)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close() 