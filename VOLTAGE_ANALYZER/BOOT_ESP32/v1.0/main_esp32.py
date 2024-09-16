from machine import UART, Pin
import time

# UART setup for ESP32 (TX = 19, RX = 22)
uart_esp32 = UART(2, baudrate=9600, tx=Pin(19), rx=Pin(22))

# Function to send a command and wait for a response
def send_command(command):
    uart_esp32.write(command + '\n')  # Send the command with newline character
    time.sleep(1)  # Give some time for the Pico to process the request
    
    response = uart_esp32.read()  # Read the response from Pico
    if response:
        print("Response from Pico: ", response.decode('utf-8').strip())
    else:
        print("No response received")

# Main loop
while True:
    command = "READ_VOLT_0"  # Example command, can change to other pins (READ_VOLT_1, READ_VOLT_2, etc.)
    send_command(command)
    time.sleep(10)  # Wait 10 seconds before sending the next command
