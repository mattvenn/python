import csv
import webbrowser
import serial

url = 'http://uk.farnell.com/'
codes = []
scans = []
with open('order.txt') as fh:
    reader = csv.reader(fh, delimiter=' ')
    for row in reader:
        scan = row[4].replace('-','')
        code = row[0]
        print(scan + " " + code)
        scans.append(scan)
        codes.append(code)

port = '/dev/ttyACM0'
ser = serial.Serial(port)
while True:
    scan = ser.read(17)
    scan = scan[0:15]
    print(scan)
    try:
        code = codes[scans.index(scan)]
        print(code)
        webbrowser.open_new_tab(url + code)
    except ValueError:
        print("no code found")
