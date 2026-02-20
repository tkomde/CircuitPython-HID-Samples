import usb.core
import usb_host
import board
import time
import array
import adafruit_usb_host_descriptors

# Specify data-plus and data-minus pins
dp = board.GP0
dm = board.GP1

# Initialize USB host port
host_port = usb_host.Port(dp, dm)
print("USB host port initialized.")

time.sleep(1.5)

# Array to store key inputs
input_data = []

def find_mouse():
    # Search for USB devices
    devices = list(usb.core.find(find_all=True))
    for device in devices:
        print(f"Device: {device.idVendor:04x}:{device.idProduct:04x} - {device.product} - {device.manufacturer}")

        # try to find mouse endpoint on the current device.
        mouse_interface_index, mouse_endpoint_address = (
            # adafruit_usb_host_descriptors.find_boot_mouse_endpoint(device)
            adafruit_usb_host_descriptors.find_report_mouse_endpoint(device)
        )
        if mouse_interface_index is not None and mouse_endpoint_address is not None:
            mouse = device
            endpoint_address = mouse_endpoint_address
            print(
                f"mouse interface: {mouse_interface_index} "
                + f"endpoint_address: {hex(mouse_endpoint_address)}"
            )
    if not devices:
        print("No USB devices found (1)")
        time.sleep(0.1) # Added: improves PnP response; avoids being too busy
        return None, None
    else:
        mouse = usb.core.find(idVendor=device.idVendor, idProduct=device.idProduct)
        if mouse is None:
            print("No USB devices found (2). Retrying.")
            time.sleep(0.5)
        else:
            print("USB device found.")

            # Required to read scroll data from the mouse
            # https://github.com/adafruit/circuitpython/issues/10159
            REQDIR_HOSTTODEVICE = 0
            REQTYPE_CLASS = 1 << 5
            REQREC_INTERFACE = 1 << 0
            HID_REQ_SetProtocol = 0x0B

            bmRequestType = (REQDIR_HOSTTODEVICE | REQTYPE_CLASS | REQREC_INTERFACE)
            bRequest = HID_REQ_SetProtocol
            wValue = 1
            wIndex = 0

            try:
                buf = bytearray(1)
                num = mouse.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, buf)
            except usb.core.USBError:
                print("TRANSFER CONTROL ERROR")

            mouse.set_configuration()
        return mouse, endpoint_address 

# Key input loop
mouse = None
buf = array.array("b", [0] * 4)

while True:
    if mouse is None:
        print("Searching for mouse...")
        mouse, endpoint_address = find_mouse()
        continue

    try:
        num_bytes = mouse.read(endpoint_address, buf)
        print(f"RAW data: {list(buf)}")  # For now, display raw data
    except Exception as e:
        print(f"Error: {e}")
        mouse = None
        time.sleep(1)
