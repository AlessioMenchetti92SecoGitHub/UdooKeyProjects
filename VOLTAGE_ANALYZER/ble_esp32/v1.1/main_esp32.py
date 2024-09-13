import ubluetooth
from machine import Pin, UART
from time import sleep

# Definizione dei pin dei LED
LED_PIN_YELLOW = 33  # Yellow LED
LED_PIN_BLUE = 32    # Blue LED

# Inizializza i pin LED come output
led_yellow = Pin(LED_PIN_YELLOW, Pin.OUT)
led_blue = Pin(LED_PIN_BLUE, Pin.OUT)

# Configurazione UART per la comunicazione con il Raspberry Pi Pico (TX=19, RX=22)
uart_esp32 = UART(2, baudrate=9600, tx=Pin(19), rx=Pin(22))

class BLEServer:
    def __init__(self, name="ESP32_Controller"):
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.register_services()
        self.advertise(name)

    def ble_irq(self, event, data):
        if event == 1:  # Evento di connessione
            print("Device connected")
        elif event == 2:  # Evento di disconnessione
            print("Device disconnected")
            # Dopo una disconnessione, riavviamo la pubblicità BLE
            self.advertise("ESP32_Controller")
        elif event == 3:  # Evento di ricezione di dati
            buffer = self.ble.gatts_read(self.rx_handle)
            command = buffer.decode('utf-8').strip()
            print(f"Received command: {command}")
            self.process_command(command)

    def register_services(self):
        # UUID del servizio e della caratteristica
        SERVICE_UUID = ubluetooth.UUID(0x180F)
        CHAR_UUID = ubluetooth.UUID(0x2A19)
        char = (CHAR_UUID, ubluetooth.FLAG_WRITE | ubluetooth.FLAG_WRITE_NO_RESPONSE | ubluetooth.FLAG_READ,)
        service = (SERVICE_UUID, (char,))

        # Registra il servizio e la caratteristica
        ((self.rx_handle,),) = self.ble.gatts_register_services((service,))
        print("Service and Characteristic Registered")

    def advertise(self, name):
        # Pubblicizza il nome del dispositivo
        name = bytes(name, 'utf-8')
        adv_data = bytearray(b'\x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(f"Advertising as: {name.decode('utf-8')}")

    def process_command(self, command):
        # Accendi o spegni i LED in base ai comandi ricevuti
        if command == "YELLOW_ON":
            led_yellow.value(1)
            print("Yellow LED ON")
        elif command == "YELLOW_OFF":
            led_yellow.value(0)
            print("Yellow LED OFF")
        elif command == "BLUE_ON":
            led_blue.value(1)
            print("Blue LED ON")
        elif command == "BLUE_OFF":
            led_blue.value(0)
            print("Blue LED OFF")
        elif command.startswith("READ_VOLT_"):
            # Invia comando al Raspberry Pi Pico tramite UART
            uart_esp32.write(command + '\n')
            sleep(1)  # Attendi per la risposta
            response = uart_esp32.read()
            if response:
                # Trasmetti la risposta via BLE
                response_str = response.decode('utf-8').strip()
                print(f"Received from Pico: {response_str}")
                self.ble.gatts_write(self.rx_handle, response_str.encode('utf-8'))
            else:
                print("No response from Pico")
        else:
            print("Unknown command")

# Inizializza il server BLE e pubblicizza
ble_server = BLEServer(name="ESP32_Controller")

# Loop principale
while True:
    sleep(1)
