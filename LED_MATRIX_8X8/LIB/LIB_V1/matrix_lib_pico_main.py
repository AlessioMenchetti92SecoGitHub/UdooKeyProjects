'''
Version 1:
-base funtionalities
-code review
-insert possibility to print a string character per character
'''
from machine import Pin, SPI
import max7219
from time import sleep

#Setting variables
CHANNEL_SPI = 0
BAUD_RATE = 1200
POLARITY=0
PHASE=0
CS_PIN = 15
BRIGHTNESS = 5
# Configura SPI e il display ---- Configuration SPI and Display
spi = SPI(CHANNEL_SPI, baudrate=BAUD_RATE, polarity=POLARITY, phase=PHASE)
cs = Pin(CS_PIN, Pin.OUT)

# Configura la matrice LED 8x8 ---- Configuration led matrix 8x8
display = max7219.Matrix8x8(spi, cs, 1)
display.brightness(BRIGHTNESS)  # Imposta la luminosità (0 a 15) ---- Brightness (0 until 15)

def display_char(text):
    """
    Mostra un carattere sulla matrice LED.
    Show char in a led matrix
    """
    display.text(text[0], 0, 0, 1)  # Text, x, y, color
    display.show()

def display_str(text,delay_char_sec=3):
    '''
    Mostra l'intera stringa carattere per carattere con un certo ritardo
    '''
    for ch in str(text):
        print(f'Display {ch}')
        display_char(ch)
        sleep(delay_char_sec)

def main():
    #Pulizia iniziale ---- Initial clean
    print('Initial clean display')
    display_char(' ')
    
    while True:#Loop execution
         user_input = input("String input: ").upper()
         display_str(str(user_input),delay_char_sec=1)
         display.fill(0)
         display.show()

if __name__ == "__main__":
    main()
