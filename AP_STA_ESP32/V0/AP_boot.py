'''
Access Point esp32
'''

import network
import socket

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

# Configura l'ESP32 come Access Point ---- Set up the ESP32 as an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
#ap.config(essid='ESP32_AP', password='12345678') #Password  
ap.config(essid='ESP32_AP')

# Stampa l'IP dell'AP ---- Print the IP of the Access Point
print('IP Address:', ap.ifconfig()[0])

# Crea un server TCP ---- Create a TCP server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print_lng(message=['Server in ascolto...','Server listening...'])

while True:
    cl, addr = s.accept()
    print_lng(message=[f'Client connesso da {addr}',f'Client connected from {addr}'])
    while True:
        data = cl.recv(1024)
        if not data:
            break
        print_lng(f'Ricevuto {data}',f'Receive {data}')
        cl.send(b'Hello from Server')
    cl.close()
    print('Client disconnesso')
    print_lng(message=['Client disconnesso','Client disconnected'])
