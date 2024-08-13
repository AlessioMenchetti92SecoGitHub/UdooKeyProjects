'''
Blink esp32 Udoo Key
'''

from machine import Pin
from time import sleep_ms

state_log = True #If true print the state of led

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

#LED settings
LED_PIN_YELLOW = 33 #Yellow led of Udoo Key
LED_PIN_BLUE = 32 #Blue led of Udoo Key

led_yellow = Pin(LED_PIN_YELLOW,Pin.OUT)
led_blue = Pin(LED_PIN_BLUE,Pin.OUT) #Not using in this version 

#Time sleep
delay_time = 500 #in ms

#Message config
if state_log == True:
   print(f'Pin yellow led {led_yellow};\n Pin blue led {led_blue};\n Time sleep {delay_time} ms')

#Control loop
while True:
    
    #Yellow LED control
    led_yellow.on()
    if state_log == True:
       print_lng(message=['LED giallo acceso','Yellow LED on'])
    sleep_ms(delay_time)
    led_yellow.off()
    if state_log == True:
       print_lng(message=['LED giallo spento','Yellow LED off'])
    sleep_ms(delay_time)

    #Blue LED control
    led_yellow.on()
    if state_log == True:
       print_lng(message=['LED blue acceso','Blue LED on'])
    sleep_ms(delay_time)
    led_yellow.off()
    if state_log == True:
       print_lng(message=['LED blue spento','Blue LED off'])
    sleep_ms(delay_time)