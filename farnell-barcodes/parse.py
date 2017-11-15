
WAIT = 0
ORDER_STARTED = 1
ORDER_FINISHED = 2

def parse(filename):
    orders = []
    state = WAIT
    last_line = ""

    # parse the text into lines
    with open(filename) as fh:
        while True:
            if state == WAIT:
                line = fh.readline()
                # end of file
                if line == "":
                    break
                elif line.startswith('TC') or line.startswith('UD'):
                    state = ORDER_STARTED
                    l = 0
                    order = last_line
            elif state == ORDER_STARTED:
                line = fh.readline()
                if l > 1:
                    state = ORDER_FINISHED
                order += line
                l += 1
            elif state == ORDER_FINISHED:
                orders.append(order)
                state = WAIT
            last_line = line     


    print("%d lines read from %s" % (len(orders), filename))
    # now get the details from each line
    codes  = []
    scans = []
    order_num = 1
    for order in orders:
        lines = order.split('\n')
        code = lines[0]
        scan = lines[2].replace('Despatch Note No ', '')
        scan = scan.replace('-', '')
        scan += "%03d" % order_num
        order_num += 1
        print(code, scan)
        codes.append(code)
        scans.append(scan)
    return codes, scans
