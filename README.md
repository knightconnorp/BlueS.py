# BlueS.py
BlueS.py - Bluetooth Low Energy (BLE) Sniffer<br>

Displays MAC Address, RSSI, Device Name, Company, and Last Seen Time in one simple table<br>
Ability to save table as CSV for later analysis and viewing<br>

## Steps
Step 1 - Connect Alfa Card (or alternative BLE adapter)<br>
Step 2 - Use 'iwconfig' (on linux) to ensure your device is detecting your wireless card<br>
Step 3 - (If execution bit not set) chmod +x BlueS.py<br>
Step 4 - Run as sudo/root<br>

## Options
-h OR --help         Help menu<br>
-o <filename>        Save output as CSV on exit<br>
-n                   Must broadcast name of device<br>
-c                   Must broadcast device manufacturer<br>
-m <mac_address>     Hunt on a specific mac address, highlights in RED<br>
-i <hci_interface>   Specify hci interface to use in scan<br>
-s <scan_length>     Specify scan length in seconds

## Dependencies
Run these commands in your linux environment 
> sudo apt-get install build-essential libglib2.0-dev python3 pip python3-dev<br><br>
> pip install bluepy prettytable<br>

![Screenshot of BlueS.py running](/BlueSpy0.png)
![Screenshot of BlueS.py running](/BlueSpy1.png)
