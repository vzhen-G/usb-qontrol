import usb.core
import usb.util
import time
import re

# define the values format
value_format = '\d+\.\d+'
nup_format = ''


# find the device
device = usb.core.find(idVendor = 0x0403,idProduct = 0x6001)
if device is None:
    raise ValueError('Device not found')

device.set_configuration()
# get an endpoint instance
cfg = device.get_active_configuration()
intf = cfg[(0,0)]
ep = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)
assert ep is not None

# write the data
res = ep.write('nupall?\n')
time.sleep(1)
print(res)
#read the response of Qontrol
nupresult = ep.read(1024)

nup = str(nupresult, encoding="ascii")
print(nup) # debug

matchobj = re.match(value_format, '5.5')
if matchobj:
    print(matchobj)
else:
    print("error")



