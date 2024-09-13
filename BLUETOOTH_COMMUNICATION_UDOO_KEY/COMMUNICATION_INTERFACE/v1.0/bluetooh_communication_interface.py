import asyncio
from bleak import BleakClient, BleakScanner
import tkinter as tk
from tkinter import ttk

# Indirizzo MAC del tuo dispositivo ESP32 (puoi trovarlo con un'app tipo nRF Connect)
DEVICE_MAC_ADDRESS = "8C:4B:14:CB:C6:5A"  # Inserisci l'indirizzo MAC del tuo ESP32

# UUID del servizio e della caratteristica che usi (da BLEServer)
SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

# Crea un loop per gestire le chiamate asincrone
loop = asyncio.get_event_loop()

# Funzione per inviare comandi BLE
async def send_command(command):
    try:
        async with BleakClient(DEVICE_MAC_ADDRESS, timeout=10.0) as client:
            if client.is_connected:
                status_label.config(text="Connesso", bg="green")
                print(f"Sending command: {command}")
                await client.write_gatt_char(CHARACTERISTIC_UUID, command.encode('utf-8'))
                #client.disconnect()
            else:
                status_label.config(text="Disconnesso", bg="red")
    except Exception as e:
        status_label.config(text="Errore di connessione", bg="red")
        print(f"Failed to connect: {e}")

# Funzione che gestisce l'invio del comando
def send_command_handler():
    command = command_var.get()
    loop.create_task(send_command(command))

# Funzione per cercare e connettere al dispositivo (opzionale, per vedere i dispositivi)
async def scan_for_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)

# Interfaccia grafica con tkinter
root = tk.Tk()
root.title("Controllo ESP32 con Bluetooth")

# Luce verde per indicare lo stato di connessione
status_label = tk.Label(root, text="Disconnesso", bg="red", width=20)
status_label.grid(row=0, column=0, padx=10, pady=10)

# Menu a tendina per selezionare il comando
command_var = tk.StringVar()
commands = ["YELLOW_ON", "YELLOW_OFF", "BLUE_ON", "BLUE_OFF"]
command_menu = ttk.Combobox(root, textvariable=command_var, values=commands)
command_menu.grid(row=1, column=0, padx=10, pady=10)
command_menu.current(0)  # Seleziona il primo comando per default

# Pulsante per inviare il comando
send_button = tk.Button(root, text="Invia Comando", command=send_command_handler)
send_button.grid(row=2, column=0, padx=10, pady=10)

# Integrazione del loop asyncio nel loop tkinter
def tkinter_loop():
    loop.call_soon(loop.stop)
    loop.run_forever()
    root.after(100, tkinter_loop)

# Avvio del ciclo tkinter
root.after(100, tkinter_loop)
root.mainloop()
