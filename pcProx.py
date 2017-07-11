
#
# pcProx Reader Demo with Python by Sawahashi
# 
# Required: Python > 3, libusb
#
# Should work on Windows and Linux
# You may need to change VENDER_ID and PRODUCT_ID corresponding to your reader model
#

import usb.core
import usb.util
import time


def getProx():

    ### CONFIG
    ### You may need to change VENDER_ID and PRODUCT_ID corresponding to a reader model
    VENDER_ID = 0x0C27
    PRODUCT_ID = 0x3BFA
    PROX_END = 2
    INTERFACE = 0

    # Detect the device
    dev = usb.core.find(idVendor=VENDER_ID, idProduct=PRODUCT_ID)
    if dev is None:
        raise ValueError('Card reader is not connected')

    # Make sure libusb handles the device
    if dev.is_kernel_driver_active(INTERFACE):
        print('Detach Kernel Driver')
        dev.detach_kernel_driver(INTERFACE)

    # Set a mode
    # ctrl_transfer is used to control endpoint0
    dev.set_configuration(1)
    usb.util.claim_interface(dev, INTERFACE)
    dev.ctrl_transfer(0x21, 9, 0x0300, 0, [0x008d]) 

    # Pull the status
    output = dev.ctrl_transfer(0xA1, 1, 0x0300, 0, PROX_END)

    # Convert output into integers
    proxHex = '0x'
    for h in reversed(output):
        proxHex += hex(h)[2:]

    return int(proxHex, 16)


### Main Loop

prev = 0
print('Ready for Scan...')

while 1:
    result = getProx()
    if(result != prev):
        if(result != 0):
            print(result)
        prev = result

    time.sleep(0.3);

