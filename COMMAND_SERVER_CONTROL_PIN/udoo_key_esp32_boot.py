import network
import socket
from machine import Pin, UART
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

# Setting channel Uart 
CH_UART = 0

# Setting Pin UART tx e rx
# U_K_ means Udoo Key
U_K_TX = 19
U_K_RX = 22

# Setting baud rate
BAUD_RATE = 1200

# Credenziali rete Wi-Fi ---- Credential Wi-Fi network
ssid = 'ID_WIFI'
password = 'PSW'

# Configurazione Wi-Fi ---- Configuration Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

#Tentativi di connessine alla rete ---- Attempts to connect to the network
while not station.isconnected():
    print('Connessione in corso...')
    time.sleep(1)

# Ottieni l'indirizzo IP ---- Obtain IP address
ip = station.ifconfig()[0]
print('Connessione stabilita, IP:', ip)

# Configurazione UART ---- Setting UART
uart = UART(CH_UART, baudrate=BAUD_RATE, tx=U_K_TX, rx=U_K_RX)

# Configurazione dei pin per invio comandi (virtuali) ---- Pin configuration for sending (virtual) commands
pins = {
    1: "PIN1",
    2: "PIN2",
    3: "PIN3",
    4: "PIN4",
    5: "PIN5"
}

# Funzione per generare la pagina web ---- Function to generate the web page
def web_page():
    html = f"""
    <html>
    <head>
        <title>ESP32 Web Server</title>
        <style>
            body {{ font-family: Arial; text-align: center; }}
            h1 {{ color: #333; }}
            button {{ padding: 10px 20px; margin: 10px; font-size: 16px; }}
        </style>
    </head>
    <body>
        <h1>Contol GPIO Udoo Key</h1>
        <form action="/?pin=1&state=on" method="post">
            <button type="submit">Turn on PIN 1</button>
        </form>
        <form action="/?pin=1&state=off" method="post">
            <button type="submit">Turn off PIN 1</button>
        </form>
        <form action="/?pin=2&state=on" method="post">
            <button type="submit">Turn on PIN 2</button>
        </form>
        <form action="/?pin=2&state=off" method="post">
            <button type="submit">Turn off PIN 2</button>
        </form>
        <form action="/?pin=3&state=on" method="post">
            <button type="submit">Turn on PIN 3</button>
        </form>
        <form action="/?pin=3&state=off" method="post">
            <button type="submit">Turn off PIN 3</button>
        </form>
        <form action="/?pin=4&state=on" method="post">
            <button type="submit">Turn on PIN 4</button>
        </form>
        <form action="/?pin=4&state=off" method="post">
            <button type="submit">Turn off PIN 4</button>
        </form>
        <form action="/?pin=5&state=on" method="post">
            <button type="submit">Turn on PIN 5</button>
        </form>
        <form action="/?pin=5&state=off" method="post">
            <button type="submit">Turn off PIN 5</button>
        </form>
    </body>
    </html>
    """
    return html

# Funzione per inviare il comando via UART ---- Function to send the command via UART
def send_command(pin, state):
    command = f"{pin}:{state}\n"
    uart.write(command)
    print(f"Comando inviato: {command}")

# Funzione per avviare il server web ---- Function to start the web server
def serve():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Server in ascolto su', addr)

    while True:
        conn, addr = s.accept()
        print('Connessione da', addr)
        request = conn.recv(1024)
        request = str(request)
        print('Contenuto della richiesta:', request)

        if 'pin=' in request and 'state=' in request:
            pin = int(request.split('pin=')[1].split('&')[0])
            state = request.split('state=')[1].split(' ')[0]
            if pin in pins:
                send_command(pins[pin], state)
        
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

# Avvia il server ---- Start the server
serve()