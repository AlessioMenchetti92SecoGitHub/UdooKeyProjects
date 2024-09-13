import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import asyncio
from bleak import BleakClient
import threading

# Inserisci qui l'indirizzo MAC del tuo dispositivo BLE
DEVICE_MAC_ADDRESS = "8C:4B:14:CB:C6:5A"  # Cambia con l'indirizzo MAC del tuo dispositivo

# UUID della caratteristica BLE per inviare e ricevere comandi
CHAR_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

# Funzione asincrona per inviare il comando via BLE e ricevere i dati (se richiesto)
async def send_ble_command_async(command, result_callback):
    async with BleakClient(DEVICE_MAC_ADDRESS) as client:
        if await client.is_connected():
            print(f"Connesso a {DEVICE_MAC_ADDRESS}")
            
            # Invia il comando al dispositivo BLE
            await client.write_gatt_char(CHAR_UUID, command.encode('utf-8'))
            
            # Se il comando è per leggere i dati, attendi una risposta
            if command.startswith("READ_VOLT_"):
                await asyncio.sleep(1)  # Attendi per la risposta
                response = await client.read_gatt_char(CHAR_UUID)
                
                # Decodifica e ritorna la risposta
                result_callback(response.decode('utf-8').strip())
            else:
                # Per altri comandi (LED), non è necessaria una risposta
                result_callback(None)

def send_ble_command(command):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_ble_command_async(command, handle_ble_result))

# Callback per gestire i risultati BLE e aggiornare l'interfaccia
def handle_ble_result(result):
    if result:
        data_list = list(map(float, result.split(',')))

        # Mostra la media separatamente
        avg_voltage.set(f"Media Tensione: {data_list[0]:.2f} V")

        # Plot delle letture
        plot_readings(data_list[1:])  # Escludi la media per il grafico
    else:
        status_message.set(f"Comando inviato con successo")

# Funzione per gestire l'invio del comando
def send_command():
    selected_command = combo_box.get()
    threading.Thread(target=send_ble_command, args=(selected_command,)).start()

# Funzione per plottare i valori delle letture
def plot_readings(readings):
    fig.clear()  # Pulisce il grafico precedente

    ax = fig.add_subplot(111)
    ax.plot(range(1, len(readings) + 1), readings, marker='o')
    ax.set_title("Grafico delle Letture di Tensione")
    ax.set_xlabel("Numero Lettura")
    ax.set_ylabel("Valore Tensione (V)")

    canvas.draw()

# Setup finestra principale
root = tk.Tk()
root.title("Controllo via BLE")
root.geometry("500x600")

# Menu a tendina per i comandi
commands = ["YELLOW_ON", "YELLOW_OFF", "BLUE_ON", "BLUE_OFF", "READ_VOLT_0", "READ_VOLT_1", "READ_VOLT_2"]
combo_box = ttk.Combobox(root, values=commands)
combo_box.set("Seleziona Comando")
combo_box.pack(pady=20)

# Pulsante per inviare il comando
send_button = tk.Button(root, text="Invia Comando", command=send_command)
send_button.pack(pady=10)

# Etichetta per la media della tensione
avg_voltage = tk.StringVar()
avg_label = tk.Label(root, textvariable=avg_voltage, font=("Arial", 14))
avg_label.pack(pady=10)

# Etichetta per lo stato dei LED
status_message = tk.StringVar()
status_label = tk.Label(root, textvariable=status_message, font=("Arial", 12))
status_label.pack(pady=10)

# Creare un grafico vuoto inizialmente
fig = plt.Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Loop principale
root.mainloop()
