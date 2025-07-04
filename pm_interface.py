from ThorlabsPM100 import ThorlabsPM100
import usb.core
import usb.util

dev = usb.core.find(idVendor=0x1313, idProduct=0x8075)
if dev is None:
    raise ValueError("pm400 not found")

pm = ThorlabsPM100(inst = dev)
print(pm.measure.scalar.voltage)
