import network
import time
import dht
import machine
import utime
import os
from bmp180 import BMP180
from umqtt.simple import MQTTClient


DHT11_PIN=5
RAIN_PIN=13
DELAY=1
last_mesurement_time = 0
#year=99; month=0; day=0; hour=0; minute=0; second=0; ms=0; dayinyear=0; t=0; h=0; l=0
rain=''
rtc=machine.RTC()
rtc.datetime((2020, 2, 16, 7, 19, 12, 0, 0))
#t=0; h=0; l=0
j=0
RainSensor=machine.Pin(RAIN_PIN, machine.Pin.IN)
LightSensor=machine.ADC(0)
bus =  machine.I2C(scl=machine.Pin(14), sda=machine.Pin(12), freq=100000)   # on esp8266


bmp180 = BMP180(bus)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

WiFi_SSID = "5T"
WiFi_PASS = "12345678"

SERVER = "mqtt.thingspeak.com"
client = MQTTClient("umqtt_client", SERVER)

CHANNEL_ID = "992282"
WRITE_API_KEY = "T0C09N6ZGNLAZUSD"

topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY

f=open('datos.txt','w')
f.close()

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WiFi_SSID, WiFi_PASS)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def mesure_temperature_and_humidity():
    d = dht.DHT11(machine.Pin(DHT11_PIN))
    d.measure()
    t = d.temperature()
    h = d.humidity()
    
    temp = bmp180.temperature
    
    print('Temperature = %.2f degC (DHT11) or %.2f degC (BMP180)' % (t,temp))
    print('Humidity    = %.2f percent' % h)
    
    #f=open('datos.txt','a')
    #f.write('Temperature = %.2f (DHT11) or %.2f (BMP180)' % (t,temp))
    #f.write(' Humidity = %.2f p ' % h)
    #f.close()
    
    return t,h,temp
    
def measure_rain():
  r=RainSensor.value()
  if r==0:
    rain='YES'
    ra=True
  else:
    rain='NO'
    ra=False
  print('Raining     = %s' % rain) 
  #f=open('datos.txt','a')
  #f.write(' Raining = %s ' % rain)
  #f.close()
  return int(ra)
  
def measure_light():
  l=LightSensor.read()
  l=l*100/1023
  print('Light       = %d percent' % l)  
  #f=open('datos.txt','a')
  #f.write('Light = %d p' % l)
  #f.close()
  return l

def pressure():
  p = bmp180.pressure
  altitude = bmp180.altitude
  print("Pressure    = %.2f Pa" %p)
  print("Altitude    = %.2f m" %altitude)
  #f=open('datos.txt','a')
  #f.write("Pressure = %.2f Pa " %p)
  #f.write("Altitude = %.2f m" %altitude)
  #f.close()
  return p,altitude
  
def date():
  year, month, day, hour, minute, second, ms, dayinyear = utime.localtime()
  print('\nDate = %d/%d/%d %d:%d:%d' % (year, month, day, hour, minute, second))
  #f=open('datos.txt','a')
  #f.write('\nDate: %d/%d/%d %d:%d:%d ' % (year, month, day, hour, minute, second))
  #f.close()
 
def save_data():
  global j
  j+=1
  if j==5:
    os.remove('datos.txt')
    j=1
  
do_connect()
while True:
    current_time = time.time()
    
    if current_time - last_mesurement_time > 15:
        
        date()
        t,h,temp = mesure_temperature_and_humidity()
        rain = measure_rain()
        l = measure_light()
        #save_data()
        p,altitude = pressure()
        last_mesurement_time = current_time
        
        payload = "field2="+str(temp)+"&field3="+str(h)+"&field4="+str(l)+"&field5="+str(p)+"&field6="+str(altitude)
        
        client.connect()
        client.publish(topic, payload)
        client.disconnect() 
        
    time.sleep(DELAY)


