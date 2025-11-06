import time
import struct

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
# from adafruit_hid.keyboard import Keyboard
# from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
# from adafruit_hid.keycode import Keycode
# from adafruit_hid.mouse import Mouse
# from adafruit_hid.consumer_control import ConsumerControl
# from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid import find_device

# Vendor-Defined Report (Report ID 5/6, USAGE 0xFFFE) was attached
hid_descriptor = (
    b"\x05\x01"  # Usage Page (Generic Desktop Ctrls)
    b"\x09\x06"  # Usage (Keyboard)
    b"\xa1\x01"  # Collection (Application)
    b"\x85\x01"  # Report ID (1)
    b"\x05\x07"  # Usage Page (Kbrd/Keypad)
    b"\x19\xe0"  # Usage Minimum (\xE0)
    b"\x29\xe7"  # Usage Maximum (\xE7)
    b"\x15\x00"  # Logical Minimum (0)
    b"\x25\x01"  # Logical Maximum (1)
    b"\x75\x01"  # Report Size (1)
    b"\x95\x08"  # Report Count (8)
    # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    b"\x81\x02"
    # Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    b"\x81\x01"
    b"\x19\x00"  # Usage Minimum (\x00)
    b"\x29\x89"  # Usage Maximum (\x89)
    b"\x15\x00"  # Logical Minimum (0)
    b"\x25\x89"  # Logical Maximum (137)
    b"\x75\x08"  # Report Size (8)
    b"\x95\x06"  # Report Count (6)
    # Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    b"\x81\x00"
    b"\x05\x08"  # Usage Page (LEDs)
    b"\x19\x01"  # Usage Minimum (Num Lock)
    b"\x29\x05"  # Usage Maximum (Kana)
    b"\x15\x00"  # Logical Minimum (0)
    b"\x25\x01"  # Logical Maximum (1)
    b"\x75\x01"  # Report Size (1)
    b"\x95\x05"  # Report Count (5)
    # Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
    b"\x91\x02"
    b"\x95\x03"  # Report Count (3)
    # Output (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
    b"\x91\x01"
    b"\xc0"  # End Collection
    b"\x05\x01"  # Usage Page (Generic Desktop Ctrls)
    b"\x09\x02"  # Usage (Mouse)
    b"\xa1\x01"  # Collection (Application)
    b"\x09\x01"  # Usage (Pointer)
    b"\xa1\x00"  # Collection (Physical)
    b"\x85\x02"  # Report ID (2)
    b"\x05\x09"  # Usage Page (Button)
    b"\x19\x01"  # Usage Minimum (\x01)
    b"\x29\x05"  # Usage Maximum (\x05)
    b"\x15\x00"  # Logical Minimum (0)
    b"\x25\x01"  # Logical Maximum (1)
    b"\x95\x05"  # Report Count (5)
    b"\x75\x01"  # Report Size (1)
    # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    b"\x81\x02"
    b"\x95\x01"  # Report Count (1)
    b"\x75\x03"  # Report Size (3)
    # Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    b"\x81\x01"
    b"\x05\x01"  # Usage Page (Generic Desktop Ctrls)
    b"\x09\x30"  # Usage (X)
    b"\x09\x31"  # Usage (Y)
    b"\x15\x81"  # Logical Minimum (-127)
    b"\x25\x7f"  # Logical Maximum (127)
    b"\x75\x08"  # Report Size (8)
    b"\x95\x02"  # Report Count (2)
    # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    b"\x81\x06"
    b"\x09\x38"  # Usage (Wheel)
    b"\x15\x81"  # Logical Minimum (-127)
    b"\x25\x7f"  # Logical Maximum (127)
    b"\x75\x08"  # Report Size (8)
    b"\x95\x01"  # Report Count (1)
    # Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position)
    b"\x81\x06"
    b"\xc0"  # End Collection
    b"\xc0"  # End Collection
    b"\x05\x0c"  # Usage Page (Consumer)
    b"\x09\x01"  # Usage (Consumer Control)
    b"\xa1\x01"  # Collection (Application)
    b"\x85\x03"  # Report ID (3)
    b"\x75\x10"  # Report Size (16)
    b"\x95\x01"  # Report Count (1)
    b"\x15\x01"  # Logical Minimum (1)
    b"\x26\x8c\x02"  # Logical Maximum (652)
    b"\x19\x01"  # Usage Minimum (Consumer Control)
    b"\x2a\x8c\x02"  # Usage Maximum (AC Send)
    # Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    b"\x81\x00"
    b"\xc0"  # End Collection
    b"\x06\xfe\xff"  # Usage Page (Vendor-defined: 0xFFFE)
    b"\x09\x01"  # Usage (Vendor Usage 1)
    b"\xa1\x01"  # Collection (Application)
    b"\x85\x05"  # Report ID (5)
    b"\x15\x00"  # Logical Minimum (0)
    b"\x25\xff"  # Logical Maximum (255)
    b"\x75\x08"  # Report Size (8)
    b"\x95\x01"  # Report Count (1)
    b"\x09\x01"  # Usage (Vendor Usage 1 for Input)
    b"\x81\x02"  # Input (Data,Var,Abs)
    b"\x09\x01"  # Usage (Vendor Usage 1 for Output)
    b"\x91\x02"  # Output (Data,Var,Abs)
    b"\xc0"  # End Collection
    # -- Vendor-defined Report (Report ID 6) --
    # usage_page / usage same as Report ID 5 (0xFFFE, 0x01)
    b"\x06\xfe\xff"  # Usage Page (Vendor-defined: 0xFFFE)
    b"\x09\x01"  # Usage (Vendor Usage 1)
    b"\xa1\x01"  # Collection (Application)
    b"\x85\x06"  # Report ID (6)
    b"\x15\x00"  # Logical Minimum (0)
    b"\x26\xff\xff"  # Logical Maximum (65535) (2-byte)
    b"\x75\x10"  # Report Size (16)
    b"\x95\x01"  # Report Count (1)
    b"\x09\x01"  # Usage (Vendor Usage 1 for Input)
    b"\x81\x02"  # Input (Data,Var,Abs) -- 16-bit input
    b"\x09\x01"  # Usage (Vendor Usage 1 for Output)
    b"\x91\x02"  # Output (Data,Var,Abs) -- 16-bit output
    b"\xc0"  # End Collection
)
hid = HIDService(hid_descriptor=hid_descriptor)
device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
# Advertise as "Keyboard" (0x03C1) icon when pairing
# https://www.bluetooth.com/specifications/assigned-numbers/
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "CP_HID"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected")
    print(ble.connections)

# k = Keyboard(hid.devices)
# kl = KeyboardLayoutUS(k)
# cc = ConsumerControl(hid.devices)
# m = Mouse(hid.devices)
vd = find_device(hid.devices, usage_page=0xfe, usage=0x01)

while True:
    ite = 0
    while not ble.connected:
        pass
    print("Start typing:")

    while ble.connected:
        while (ite < 100):
            print("ite:", ite)
            # k.send(Keycode.SHIFT, Keycode.L)  # add shift modifier
            # cc.press(ConsumerControlCode.VOLUME_DECREMENT)
            # cc.release()
            # m.move(x=4, y=2)
            to_send_1b = bytearray(1)
            struct.pack_into("<B", to_send_1b, 0, ite)  # sample 1byte data
            vd.send_report(to_send_1b, 5)
            time.sleep(0.1)
            to_send_2b = bytearray(2)
            struct.pack_into("<H", to_send_2b, 0, ite +
                             0x1200)  # sample 2bytes data
            vd.send_report(to_send_2b, 6)
            time.sleep(1)
            print(f"read(id5): {vd.get_last_received_report(5)}")
            print(f"read(id6): {vd.get_last_received_report(6)}")
            ite += 1

    ble.start_advertising(advertisement)
