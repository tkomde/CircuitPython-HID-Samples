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

telephony = usb_hid.Device(
    report_descriptor=bytes((
        b"\x05\x0B"  # USAGE_PAGE (Telephony Devices)
        b"\x09\x05"  # USAGE (Headset)
        b"\xA1\x01"  # COLLECTION (Application)
        b"\x85\x01"  # REPORT_ID (1)
        b"\x15\x00"  # LOGICAL_MINIMUM (0)
        b"\x25\x01"  # LOGICAL_MAXIMUM (1)
        b"\x75\x01"  # REPORT_SIZE (1)
        b"\x95\x02"  # REPORT_COUNT (2)
        b"\x09\x20"  # USAGE (Hook Switch)
        b"\x09\x2F"  # USAGE (Phone Mute)
        b"\x81\x02"  # INPUT (Data, Variable, Absolute)
        b"\x95\x06"  # REPORT_COUNT (6)
        b"\x81\x03"  # INPUT (Constant, Variable, Absolute)
        b"\x85\x02"  # REPORT_ID (2)
        b"\x15\x00"  # LOGICAL_MINIMUM (0)
        b"\x25\x01"  # LOGICAL_MAXIMUM (1)
        b"\x75\x01"  # REPORT_SIZE (1)
        b"\x95\x03"  # REPORT_COUNT (3)
        b"\x05\x08"  # USAGE_PAGE (LED)
        b"\x09\x47"  # USAGE (Mute LED)
        b"\x09\x48"  # USAGE (Off-Hook LED)
        b"\x09\x4B"  # USAGE (Ring LED)
        b"\x91\x02"  # OUTPUT (Data, Variable, Absolute)
        b"\x95\x05"  # REPORT_COUNT (5)
        b"\x91\x03"  # OUTPUT (Constant, Variable, Absolute)
        b"\xC0"      # END COLLECTION
    )),
    usage_page=0x0B,
    usage=0x05,
    report_ids=(0x01,0x02),
    in_report_lengths=(1,0),
    out_report_lengths=(0,1)
)

usb_hid.enable([telephony])
