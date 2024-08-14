from machine import Pin, UART

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

# Configurazione Pin tx e rx UART
U_K_TX = 0
U_K_RX = 1

# Configurazione baud rate ---- Setting Baud Rate
BAUD_RATE = 1200

# Configurazione UART 
uart = UART(0, baudrate=BAUD_RATE, tx=Pin(U_K_TX), rx=Pin(U_K_RX))

# Configurazione dei pin da controllare
pin1 = Pin(15, Pin.OUT)
pin2 = Pin(14, Pin.OUT)
pin3 = Pin(13, Pin.OUT)
pin4 = Pin(12, Pin.OUT)
pin5 = Pin(11, Pin.OUT)

pins = {
    "PIN1": pin1,
    "PIN2": pin2,
    "PIN3": pin3,
    "PIN4": pin4,
    "PIN5": pin5
}

# Funzione per controllare i pin in base ai comandi ricevuti ---- Function to control the pins based on received commands
def control_pin(pin, state):
    if state == "on":
        pins[pin].on()
    elif state == "off":
        pins[pin].off()
        
def control_pin_from_string(command):
    if ":" in command:
                pin, state = command.split(":")
                pin = pin.strip()
                state = state.strip()
                if pin in pins:
                    print_lng(message=[f'Pin selezionato {pin}; Stato da settare {state}',f'Pin selected {pin}; State to setting {state}'])
                    control_pin(pin, state)

command = ''
# Ciclo principale per leggere i comandi via UART ---- Main loop to read commands via UART
while True:
    if uart.any():
        try:
            # Leggo comando lettera per lettera finché non trovo un carattere vuoto, eseguo e pulisco la stringa di ricezione pronto per uno nuovo ---- Read the command letter by letter until a null character is found, execute it, and clear the reception string to be ready for a new command
            command_unit = uart.readline().decode('utf-8').strip()
            print_lng(message=[f'Comando ricevuto: {command_unit}',f'Receive command: {command_unit}'])
            command = command + command_unit
            if command_unit == ' ' or command_unit == '':
                print_lng(message=[f'Totale {command}',f'Total {command}'])
                control_pin_from_string(command)
                command = ''
        except UnicodeError as e:
            print(f"Error decoding: {e}")