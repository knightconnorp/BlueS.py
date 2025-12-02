#!/usr/bin/python

from bluepy.btle import Scanner, DefaultDelegate
from prettytable import PrettyTable
from datetime import datetime
import time, sys, csv, os

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            dev.last = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print(f"Discovered new device: {dev.addr}, RSSI: {dev.rssi} dBm")
        elif isNewData:
            dev.last = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print(f"Received new data from device: {dev.addr}, RSSI: {dev.rssi} dBm")

def manufacturer_info(value):
    if value[:4] == "0600":
        return "Microsoft"
    elif value[:4] == "4c00":
        return "Apple Inc."
    elif value[:4] == "8700":
        return "Garmin International, Inc."
    else:
        return value

def clear_and_print(text):
    print("\x1b[2J\x1b[H", end="", flush=True)
    print(text, end="", flush=True)

def main():
    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = ["Device Address", "RSSI (dBm)", "Device Name", "Company", "Last Seen"]

    # Initialize the scanner
    scanner = Scanner().withDelegate(ScanDelegate())

    devices_dict = {}

    print("BlueS.py is starting BLE scan...")
    time.sleep(1)
    print("CTRL + C to exit")
    time.sleep(1)

    try:
        while True:
            devices = scanner.scan(3.0) # Scan for 5 seconds

            # Clear the table and update it with new data
            table.clear_rows()

            for dev in devices:
                # Get device info
                addr = dev.addr
                rssi = dev.rssi
                name = dev.getValueText(9) or 'N/A'
                company = manufacturer_info(str(dev.getValueText(255))) or 'N/A'
                last = dev.last
        
                # if device is already in table, only update RSSI
                if addr in devices_dict:
                    devices_dict[addr]["RSSI"] = rssi
                    devices_dict[addr]["Last Seen"] = last
                else:
                    devices_dict[addr] = {
                        "RSSI": rssi,
                        "Name": name,
                        "Company": company,
                        "Last Seen": last
                    }

            table.clear_rows()

            for addr, dev_info in devices_dict.items():
                table.add_row([addr, dev_info["RSSI"], dev_info["Name"], dev_info["Company"], dev_info["Last Seen"]])

            # sort
            table.sortby = "RSSI (dBm)"

            # Print the updated table
            clear_and_print(table)

            # Wait for 5 seconds before scanning again
            time.sleep(1)
    except:
        if out:
            csv_table = table.get_csv_string()
            print("Saving table as CSV...")
            with open(out_file, 'w', newline='') as f:
                f.write(csv_table)
        print("\nExiting...")

def check_sudo():
    if os.geteuid() == 0:
        pass
    else:
        print("BlueS.py MUST RUN AS ROOT/SUDO")
        sys.exit(0)

if __name__ == '__main__':
    check_sudo()
    if len(sys.argv) < 2:
        out = False
        main()
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("---------------------------------------------")
        print("BlueS.py - Bluetooth Low Eenrgy (BLE) Sniffer")
        print("Author - Cpl Connor Knight")
        print("---------------------------------------------")
        print("Ensure you have a BLE enabled device, and run")
        print("MUST RUN AS ROOT/SUDO")
        print("---------------------------------------------")
        print("-h OR --help     this menu")
        print("-o <filename>    output as CSV on exit")
        print("---------------------------------------------")
    else:
        args = sys.argv[1:]
        for arg in args:
            if arg == "-o":
                out = True
                if sys.argv[2]:
                    out_file = sys.argv[2]
                    main()
                else:
                    print("Must give output filename with -o")
                    sys.exit()
            else:
                out = False
