from bluepy.btle import Scanner, DefaultDelegate
import csv

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

def main():
    csv_file = 'scan_results.csv'
    csv_header = ['Device Address', 'Address Type', 'RSSI', 'Description', 'Value']

    # Open CSV file and write header
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

    # Initialize BLE scanner with custom delegate
    scanner = Scanner().withDelegate(ScanDelegate())

    try:
        # Scan for BLE devices for 10 seconds
        devices = scanner.scan(11.0)

        # Open CSV file in append mode and write scan results
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for dev in devices:
                device_info = [dev.addr, dev.addrType, dev.rssi]
                for (adtype, desc, value) in dev.getScanData():
                    row = device_info + [desc, value]
                    writer.writerow(row)
                    print("Data written to {}: {}".format(csv_file, row))

        print("Scan complete. Results saved to", csv_file)

    except Exception as e:
        print("Error occurred during scanning:", e)

if __name__ == "__main__":
    main()

