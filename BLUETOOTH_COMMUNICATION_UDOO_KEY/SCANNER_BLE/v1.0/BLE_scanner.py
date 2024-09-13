import asyncio
from bleak import BleakScanner

# Funzione che scansiona i dispositivi BLE e li stampa
async def scan_ble_devices():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Name: {device.name}, Address: {device.address}, RSSI: {device.rssi}")

# Esegui la scansione BLE
asyncio.run(scan_ble_devices())
