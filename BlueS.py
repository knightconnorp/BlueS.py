#!/usr/bin/python

from bluepy.btle import Scanner, DefaultDelegate
from prettytable import PrettyTable
from datetime import datetime
import time, sys, csv, os

ORANGE = '\033[33m'
RED = '\033[31m'
RESET = '\033[0m'

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            dev.last = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif isNewData:
            dev.last = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# TODO use YAML file to determine device manufacture data instead of hardcoding hex values
def manufacturer_info(value):
    if value[:4] == "0600":
        return "Microsoft"
    elif value[:4] == "4c00":
        return "Apple Inc."
    elif value[:4] == "8700":
        return "Garmin International, Inc."
    elif value[:4] == "7500":
        return "Samsung Electronics Co. Ltd."
    elif value[:4] == "e304":
        return "Under Armour"
    else:
        return value

def clear_and_print(text):
    print("\x1b[2J\x1b[H", end="", flush=True)
    print(text, end="", flush=True)

def main(scantime):
    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = ["Device Address", "RSSI (dBm)", "RSSI High", "Device Name", "Company", "Last Seen"]

    # Initialize the scanner
    if select_hci == True:
        scanner = Scanner(int(hci[-1])).withDelegate(ScanDelegate())
    elif select_hci == False:
        scanner = Scanner().withDelegate(ScanDelegate())


    devices_dict = {}

    os.system('clear')

    print("BlueS.py is starting BLE scan...")
    print("CTRL + C to exit")
    time.sleep(.5)

    try:
        while True:
            devices = scanner.scan(scantime) # Scan for 5 seconds

            # Clear the table and update it with new data
            table.clear_rows()

            # make time orange if not recently updated
            mac_list = [dev.addr for dev in devices]
            for addr in list(devices_dict.keys()):
                if addr not in mac_list:
                    devices_dict[addr]["Last Seen"] = RESET + ORANGE + dev.last + RESET

            for dev in devices:
                # Get device info

                # highlight for hunting on specific mac address
                if only_mac == True and dev.addr == search_mac:
                    addr = RED + dev.addr
                    last = dev.last + RESET

                else:
                    addr = dev.addr
                    last = dev.last

                rssi = dev.rssi
                name = dev.getValueText(9) or 'N/A'
                company = manufacturer_info(str(dev.getValueText(255))) or 'N/A'

                # if device in dictionary, update RSSI, last seen, and RSSI High
                if addr in devices_dict:
                    devices_dict[addr]["RSSI"] = rssi
                    devices_dict[addr]["Last Seen"] = last
                 
                    # if RSSI high is less than current RSSI, update
                    if devices_dict[addr]["RSSI High"] < rssi:
                        devices_dict[addr]["RSSI High"] = rssi
                else:
                    devices_dict[addr] = {
                        "RSSI": rssi,
                        "RSSI High": rssi,
                        "Name": name,
                        "Company": company,
                        "Last Seen": last
                    }

            table.clear_rows()

            # based on options provided in command, these if statements will filter results
            for addr, dev_info in devices_dict.items():
                if only_name == True and dev_info["Name"] != 'N/A' or only_name == False:
                    if only_company == True and dev_info["Company"] != 'None' or only_company == False:
                        table.add_row([addr, dev_info["RSSI"], dev_info["RSSI High"], dev_info["Name"], dev_info["Company"], dev_info["Last Seen"]])

            table.sortby = "RSSI (dBm)"

            clear_and_print(table)

            time.sleep(.1)
    except:
        os.system('clear')
        if out:
            csv_table = table.get_csv_string().replace(RED, '').replace(ORANGE, '').replace(RESET, '')
            print("\nSaving table as CSV...")
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
    
    out = False
    only_name = False
    only_company = False
    only_mac = False
    select_hci = False
    scan_time = 3.0
    error_arg = ""

    if len(sys.argv) < 2:
        main(scan_time)
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("---------------------------------------------------")
        print("BlueS.py - Bluetooth Low Eenrgy (BLE) Sniffer")
        print("Author - Cpl Connor Knight")
        print("---------------------------------------------------")
        print("Ensure you have a BLE enabled device, and run")
        print("MUST RUN AS ROOT/SUDO")
        print("The closer RSSI is to 0, the closer you are")
        print("---------------------------------------------------")
        print("Example: sudo ./BlueS.py -o output.csv -n -i hci1")
        print("---------------------------------------------------")
        print("-h OR --help         this menu")
        print("-o <filename>        output as CSV on exit")
        print("-m <mac_address>     hunt on a specific mac address")
        print("-i <hci>             specify hci (default: hci0)")
        print("-s <scan_time>       specify custom scan time")
        print("-n                   must broadcast name of device")
        print("-c                   must broadcast device manufacturer data")
        print("---------------------------------------------------")
    else:
        try:
            args = sys.argv[1:]
            for i, arg in enumerate(args):
                error_arg = arg
                if arg == "-o":
                    out = True
                    if sys.argv[i+2]:
                        out_file = sys.argv[i+2]
                if arg == "-n":
                    only_name = True
                if arg == "-c":
                    only_company = True
                if arg == "-m":
                    only_mac = True
                    if sys.argv[i+2]:
                        search_mac = sys.argv[i+2]
                if arg == "-i":
                    select_hci == True
                    if sys.argv[i+2]:
                        hci = sys.argv[i+2]
                if arg == "-s":
                    if sys.argv[i+2]:
                        scan_time = float(sys.argv[i+2])
            main(scan_time)
        except(IndexError, ValueError):
            if error_arg == "-o":
                print("Must give output filename with -o (Ex: output.csv)")
            if error_arg == "-m":
                print("Must give mac address to search for (Ex: 00:1A:2B:3C:4D:5E)")
            if error_arg == "-i":
                print("Must specify hci interface to use (Ex: hci1)")
            if error_arg == "-s":
                print("Must give scan time (Ex: 4 or 6.5)")
            sys.exit()
