import machine
import time
import ubinascii

# UART setup
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

# ADC setup (Pico has ADC on pins 26, 27, 28 -> ADC0, ADC1, ADC2 respectively)
adc_pins = {
    0: machine.ADC(26),  # ADC0
    1: machine.ADC(27),  # ADC1
    2: machine.ADC(28),  # ADC2
}

# Function to read voltage from an ADC pin
def read_voltage(adc_pin):
    raw_value = adc_pin.read_u16()  # 16-bit resolution
    voltage = raw_value * (3.3 / 65535)  # Scale to voltage (assuming 3.3V reference)
    return voltage

# Function to handle commands
def handle_command(command):
    if command.startswith("READ_VOLT_"):
        try:
            pin_number = int(command.split("_")[-1])  # Extract pin number
            if pin_number in adc_pins:
                adc = adc_pins[pin_number]
                readings = []

                # Perform 10 readings every 0.5 seconds
                for _ in range(10):
                    voltage = read_voltage(adc)
                    readings.append(voltage)
                    time.sleep(0.5)

                # Calculate average voltage
                avg_voltage = sum(readings) / len(readings)

                # Format the response string
                response = f"{avg_voltage:.2f}," + ",".join([f"{v:.2f}" for v in readings])
                uart.write(response + "\n")

            else:
                uart.write("ERROR: Invalid ADC pin\n")
        except Exception as e:
            uart.write(f"ERROR: {str(e)}\n")
    else:
        uart.write("ERROR: Invalid command\n")

# Main loop
while True:
    if uart.any():
        command = uart.read().decode('utf-8').strip()
        handle_command(command)
