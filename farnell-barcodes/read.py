import csv
import os
import webbrowser
import serial
from parse import parse

url = 'http://uk.farnell.com/'

# convert pdf to text
print("converting order.pdf to order.txt with pdftotext")
os.system('pdftotext order.pdf')
# parse the text
codes, scans = parse('order.txt')


port = '/dev/ttyACM0'
print("opening barcode reader on %s" % port)
ser = serial.Serial(port, baudrate=115200)

print("waiting for codes...")
while True:
    scan = ser.read(17)
    scan = scan[0:15]
    print(scan)
    try:
        code = codes[scans.index(scan)]
        print("opening %s in browser" % (url + code))
        webbrowser.open_new_tab(url + code)
    except ValueError:
        print("no code found")
