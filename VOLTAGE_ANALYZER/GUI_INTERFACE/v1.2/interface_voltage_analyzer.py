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
                result_callback(None)

def send_ble_command(command):
    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_ble_command_async(command, handle_ble_result))
    
    threading.Thread(target=run_async).start()

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
    send_ble_command(selected_command)

# Funzione per plottare i valori delle letture
def plot_readings(readings):
    fig.clear()  # Pulisce il grafico precedente

    ax = fig.add_subplot(111)
    ax.plot(range(1, len(readings) + 1), readings, marker='o')
    ax.set_title("Grafico delle Letture di Tensione")
    ax.set_xlabel("Numero Lettura")
    ax.set_ylabel("Valore Tensione (V)")

    canvas.draw()

# Funzione per aprire la pagina di test dei LED
def open_led_test():
    for widget in root.winfo_children():
        widget.destroy()  # Pulisci la finestra

    # Aggiungi i pulsanti per i LED
    tk.Button(root, text="Yellow ON", command=lambda: send_ble_command("YELLOW_ON")).pack(pady=5)
    tk.Button(root, text="Yellow OFF", command=lambda: send_ble_command("YELLOW_OFF")).pack(pady=5)
    tk.Button(root, text="Blue ON", command=lambda: send_ble_command("BLUE_ON")).pack(pady=5)
    tk.Button(root, text="Blue OFF", command=lambda: send_ble_command("BLUE_OFF")).pack(pady=5)
    
    # Etichetta per lo stato dei comandi
    global status_message
    status_message = tk.StringVar()
    tk.Label(root, textvariable=status_message, font=("Arial", 12)).pack(pady=10)
    
    # Pulsante per tornare alla schermata iniziale
    tk.Button(root, text="Torna al menu principale", command=setup_main_menu).pack(pady=20)

# Funzione per aprire la pagina di analisi delle tensioni
def open_voltage_analysis():
    for widget in root.winfo_children():
        widget.destroy()  # Pulisci la finestra

    # Menu a tendina per i comandi
    global combo_box
    combo_box = ttk.Combobox(root, values=["READ_VOLT_0", "READ_VOLT_1", "READ_VOLT_2"])
    combo_box.set("Seleziona Comando")
    combo_box.pack(pady=20)

    # Pulsante per inviare il comando
    tk.Button(root, text="Invia Comando", command=send_command).pack(pady=10)
    
    # Pulsante per tornare alla schermata iniziale
    tk.Button(root, text="Torna al menu principale", command=setup_main_menu).pack(pady=20)

    # Etichetta per la media della tensione
    global avg_voltage
    avg_voltage = tk.StringVar()
    tk.Label(root, textvariable=avg_voltage, font=("Arial", 14)).pack(pady=10)

    # Creare un grafico vuoto inizialmente
    global fig, canvas
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()    

# Funzione per configurare il menu principale
def setup_main_menu():
    for widget in root.winfo_children():
        widget.destroy()  # Pulisci la finestra

    tk.Button(root, text="Test dei LED", command=open_led_test).pack(pady=20)
    tk.Button(root, text="Analisi delle Tensioni", command=open_voltage_analysis).pack(pady=20)

# Setup finestra principale
root = tk.Tk()
root.title("Menu principale")
root.geometry("500x400")

# Imposta il menu principale
setup_main_menu()

# Loop principale
root.mainloop()
