'''
Station esp32
'''

from machine import Pin
import network
import socket
import time

language = 'ITA' #Substitute ENG if you want

#Funcion print language
def print_lng(message=[]):
    try:
     if language == 'ITA':
       print(message[0])
     if language == 'ENG':
       print(message[1])
    except:
      print('Error language message')

#LED di segnalazione ---- Indicator LED
LED_PIN_YELLOW = 33 #Yellow led of Udoo Key
LED_PIN_BLUE = 32 #Blue led of Udoo Key

led_yellow = Pin(LED_PIN_YELLOW,Pin.OUT)
led_blue = Pin(LED_PIN_BLUE,Pin.OUT) #Not using in this version 

# Spegnimento iniziale led ---- Initial LED shutdown
led_yellow.off()

# Configura l'ESP32 come Station ---- Set up the ESP32 as a Station
sta = network.WLAN(network.STA_IF)
sta.active(True)
#sta.connect('ESP32_AP', '12345678')
sta.connect('ESP32_AP')

# Attendi fino a quando non è connesso ---- Wait until it is connected
while not sta.isconnected():
    print_lng(message=['Connessione in corso...','Connecting...'])
    time.sleep(1)

# Stampa l'IP del client ---- Print the client's IP
print_lng(message=[ f'Connesso! IP Address: {sta.ifconfig()[0]}' , f'Connected! IP Address: {sta.ifconfig()[0]}'])

# Connetti al server TCP --- Connect to the TCP server
addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
s = socket.socket()
s.connect(addr)

# Invia un messaggio al server ---- Send a message to the server
s.send(b'Hello from Client')

# Ricevi la risposta dal server ---- Receive the response from the server
data = s.recv(1024)
print('Ricevuto dal server:', data)
print_lng(message=[ f'Connesso! IP Address: {data}' , f'Connected! IP Address: {data}'])

# Accensione led giallo ---- Turn on Yellow led
led_yellow.on()

# Chiudi la connessione ---- Close connection
s.close()
