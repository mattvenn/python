barcode on farnell bags is from the invoice
each line has a despatch code:

    LG1-006591469

Then for line_number, the barcode will read

    LG1-006591469%3d % line_number

Each line also contains the product code. So parsing the pdf and generating the table is necessary.
