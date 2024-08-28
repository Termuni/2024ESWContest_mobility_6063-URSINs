import pywinusb.hid as hid

from time import sleep
from msvcrt import kbhit


def sample_handler(data):
    print("Raw data: {0:}".format(data))


devices = hid.HidDeviceFilter().get_devices()
print(' i  par       ser  ven  prd  ver  name')
for i, dev in enumerate(devices):
    print("{0:> 3} {1:> 2} {2:>9} {3:04X} {4:04X} {5:04X}  {6:}"
          .format(i, dev.parent_instance_id, dev.serial_number, dev.vendor_id, 
                  dev.product_id, dev.version_number, dev.product_name))

selection = int(input("\nEnter number to select device (0-{})\n".format(i)))
device = devices[selection]
print("You have selected {}".format(device.product_name))
try:
    device.open()
    # set custom raw data handler
    device.set_raw_data_handler(sample_handler)

    print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
    while not kbhit() and device.is_plugged():
        # just keep the device opened to receive events
        sleep(1.5)
finally:
    device.close()