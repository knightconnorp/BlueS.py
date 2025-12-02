# BlueS.py
BlueS.py - Bluetooth Low Energy (BLE) Sniffer<br>

Displays MAC Address, RSSI, Device Name, Company, and Last Seen Time in one simple table<br>
Ability to save table as CSV for later analysis and viewing<br>

## Steps
Step 1 - Connect Alfa Card (or alternative BLE adapter)<br>
Step 2 - Use 'iwconfig' (on linux) to ensure your device is detecting your wireless card<br>
Step 3 - (If execution bit not set) chmod +x BlueS.py<br>
Step 3 - Run as sudo/root<br>

Options:<br>
-h OR --help       Help menu<br>
-o <filename>      Save output as CSV on exit<br>
