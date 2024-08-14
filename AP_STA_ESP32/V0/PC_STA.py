'''
PC Station
'''

import socket

# Configura l'indirizzo IP e la porta del server (ESP32 AP)
esp32_ip = '192.168.4.1'  # Sostituisci con l'IP del tuo ESP32
port = 80

# Crea un socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connessione al server (ESP32 AP)
try:
    s.connect((esp32_ip, port))
    print(f"Connesso all'ESP32 su {esp32_ip}:{port}")

    # Invia un messaggio al server
    s.sendall(b'Hello from PC Client')

    # Ricevi la risposta dal server
    data = s.recv(1024)
    print('Ricevuto dal server:', data.decode())

finally:
    # Chiudi la connessione
    s.close()
    print("Connessione chiusa")
