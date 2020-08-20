import usb.core
import usb.util
import time
import re
from array import array

# define the values format
value_format = '\d+\.\d+'
nup_format = ''
vfull_format = ''
error_format = ''

# find the device
heater = usb.core.find(idVendor = 0x0403,idProduct = 0x6001)
if heater is None:
    raise ValueError('Device not found')
# configuration
heater.set_configuration()
cfg = heater.get_active_configuration()
intf = cfg[(0,0)]
# get an endpoint instance out
ep_out = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)
assert ep_out is not None
# get an endpoint instance in
ep_in = usb.util.find_descriptor(
    intf,
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)
assert ep_in is not None


# write the data
ep_out.write('nupall?\n')
time.sleep(1)
# to make a read_buffer, if not do this operation, you will get an array object when read from input endpoint
read_buffer = ep_in.read(2048)
print(read_buffer)
nupresult = read_buffer.tobytes()
arr = array('B')
arr.frombytes(nupresult)
print(arr)
print(nupresult)
nup = str(nupresult, encoding="utf-8")
print(nup) # debug

if (not(re.search(nup_format, nup)) or re.search(error_format, nup) ):
    print(nup)
    print("error occurs")

subboard_num = len(re.findall(nup_format, nup))
channel_num = subboard_num * 8
info = "Info: Found "+ str(channel_num) + " channels (0~" + str(channel_num - 1)+") in the system"
print(info)

start_port = 0
end_port = channel_num - 1

v_min = 0
v_max_user = 5.0

ep_out.write("vfull?\n")
time.sleep(1)
vfull = str(ep_in.read(64),encoding = "ascii")
if (not(re.search(vfull_format, vfull)) or re.search(error_format, vfull) ):
    print(vfull)
    print("error occurs")


volt_precision = 6
done_message = "ok"


matchobj = re.match(value_format, '5.5')
if matchobj:
    print(matchobj)
else:
    print("error")



