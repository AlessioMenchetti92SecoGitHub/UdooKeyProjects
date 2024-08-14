'''
Version 0:
-base funtionalities
'''
from machine import Pin, SPI
import max7219
from time import sleep

# Configura SPI e il display ---- Configuration SPI and Display
spi = SPI(0, baudrate=10000000, polarity=0, phase=0)
cs = Pin(15, Pin.OUT)

# Configura la matrice LED 8x8 ---- Configuration led matrix 8x8
display = max7219.Matrix8x8(spi, cs, 1)
display.brightness(5)  # Imposta la luminosità (0 a 15) ---- Brightness (0 until 15)

def display_text(text):
    """Mostra un testo sulla matrice LED."""
    display.fill(0)  # Pulisci il display ---- Clean display
    display.text(text, 0, 0, 1)  # Text, x, y, color
    display.show()

def main():
    while True:
         user_input = input("Inserisci una lettera o un numero: ").upper()
         display = max7219.Matrix8x8(spi, cs, 1)
         display.brightness(5) 
         if user_input:
            display_text(user_input)
            sleep(2)

if __name__ == "__main__":
    main()
