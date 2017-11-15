# barcode driven browser for Farnell barcodes

Opens product page for a scanned Farnell bag.

Barcode on farnell bags is from the invoice. Each line has a despatch code:

    LG1-006591469

Then for line_number, the barcode will read

    LG1-006591469%3d % line_number

Each line also contains the product code. So parsing the pdf and generating the table is necessary.

Parsing is done by first converting pdf to txt, then simple stateful parser gets
each order line, and then inserts the scan and product code into 2 lists: scans
and codes.

# use

* connect barcode to USB (/dev/ttyACM0 is default)
* copy the farnell invoice to order.pdf and then run read.py

    python ./read.py

The order should be parsed (will exit on any error), and then wait for codes.
Product pages are opened in default browser.
