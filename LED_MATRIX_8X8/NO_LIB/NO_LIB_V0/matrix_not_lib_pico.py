'''
Version 0:
-Base funtionalities
'''

from machine import Pin, SPI
import time

# Configurazione della SPI ---- Configuration SPI
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))

# Configurazione del pin CS ---- Configuration pin CS (chip select)
cs = Pin(17, Pin.OUT)

# Funzione per inviare un comando al MAX7219 ---- Function to send command MAX7219
def send_cmd(register, data):
    cs.off()
    spi.write(bytearray([register, data]))
    cs.on()

# Inizializzazione del MAX7219 architettura ---- Initialization MAX7219 architecture
def init_max7219():
    send_cmd(0x09, 0x00)  # Decoding mode: no decoding
    send_cmd(0x0A, 0x03)  # Intensity: 3 (range 0x00 to 0x0F)
    send_cmd(0x0B, 0x07)  # Scan limit: display all 8 digits
    send_cmd(0x0C, 0x01)  # Shutdown register: normal operation
    send_cmd(0x0F, 0x00)  # Display test: off

# Funzione per pulire la matrice ---- Function to clean the matrix
def clear_matrix():
    for i in range(8):
        send_cmd(i + 1, 0x00)

# Funzione per visualizzare un carattere sulla matrice ---- Function to visualize character on matrix
def display_char(char):
    font = {
        'A': [0x3E, 0x09, 0x09, 0x3E, 0x00, 0x00, 0x00, 0x00],
        'B': [0x3F, 0x25, 0x25, 0x1A, 0x00, 0x00, 0x00, 0x00],
        'C': [0x1E, 0x21, 0x21, 0x12, 0x00, 0x00, 0x00, 0x00],
        '1': [0x00, 0x22, 0x3F, 0x20, 0x00, 0x00, 0x00, 0x00],
        '2': [0x32, 0x29, 0x29, 0x26, 0x00, 0x00, 0x00, 0x00],
        '3': [0x12, 0x21, 0x25, 0x1A, 0x00, 0x00, 0x00, 0x00]
    }

    if char in font:
        for i, value in enumerate(font[char]):
            send_cmd(i + 1, value)

# Inizializzazione del MAX7219 ---- Initialization MAX7219 
init_max7219()
clear_matrix()

characters = ['A', 'B', 'C', '1', '2', '3']
# Loop program
while True:
    for char in characters:
        clear_matrix()
        display_char(char)
        time.sleep(1)  # Delay 
