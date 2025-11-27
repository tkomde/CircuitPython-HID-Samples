import usb_hid


"""
import usb_midi
import storage
import usb_cdc
import microcontroller
import supervisor

# works
# supervisor.set_usb_identification(
# manufacturer="CP", product="TestPad", vid=0x046D, pid=0xC216)
#    vid=0x046D, pid=0xC218)

# Code to enable/disable Storage access every other time
# Used for troubleshooting USB Busy issues

boot_mode = microcontroller.nvm[0:1][0]

# initial boot
if (boot_mode == 0xFF):
    boot_mode = 0xFF
    microcontroller.nvm[0:1] = bytearray([0x00])

    usb_cdc.disable()
    storage.disable_usb_drive()
    supervisor.runtime.autoreload = False
    usb_midi.disable()

else:
    boot_mode = 0x00
    microcontroller.nvm[0:1] = bytearray([0xFF])

"""

gamepad = usb_hid.Device(
    report_descriptor=bytes((
        0x05, 0x01,  # Usage Page (Generic Desktop)
        0x09, 0x05,  # Usage (Gamepad)
        0xa1, 0x01,  # Collection (Application)
        0x85, 0x01,  # Report ID
        0xa1, 0x02,  # Collection (logical)
        0x05, 0x01,  # Usage Page (Generic Desktop)
        0x09, 0x30,  # Usage (X)
        0x09, 0x31,  # Usage (Y)
        0x09, 0x32,  # Usage (Z)
        0x09, 0x33,  # Usage (RX)
        0x09, 0x34,  # Usage (RY)
        0x09, 0x39,  # Usage (Hat Switch)
        0x15, 0x80,  # Logical Minimum (-128)
        0x25, 0x7F,  # Logical Maximum (127)
        0x75, 0x08,  # Report Size (8)
        0x95, 0x06,  # Report Count (6)
        0x81, 0x02,  # Input (Data, Variable, Absolute)
        0xc0,  # End Collection
        0xa1, 0x02,  # Collection (logical)
        0x05, 0x09,  # Usage Page (Button)
        0x19, 0x01,  # Usage Minimum (Button 1)
        0x29, 0x10,  # Usage Maximum (Button 16)
        0x15, 0x00,  # Logical Minimum (0)
        0x25, 0x01,  # Logical Maximum (1)
        0x75, 0x01,  # Report Size (1)
        0x95, 0x10,  # Report Count (16)
        0x81, 0x02,  # Input (Data, Variable, Absolute)
        0xc0,  # End Collection
        0xc0         # End Collection
    )),
    usage_page=0x01,
    usage=0x05,
    report_ids=(0x01,),
    in_report_lengths=(8, ),
    out_report_lengths=(0, )
)

usb_hid.enable([gamepad])
