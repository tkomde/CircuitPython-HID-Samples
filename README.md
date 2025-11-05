# CircuitPython Vendor Defined HID Sample

A sample for performing INPUT/OUTPUT communication using a Vendor Defined Usage Page for HID over BLE with Chrome's WebHID.

## Confirmed Environment

- CircuitPython: 10.1.0-beta.0
- Board: Seeed Xiao nRF52840 Sense
- Chrome: M142 (macOS / Windows)
  - ChromeOS does not work.

## Data Communication Details

- Report Map Contains..
  - Report Ids 1, 2, and 3 implement the standard Keyboard, Mouse, and Consumer Control as defined by adafruit_ble.
  - Report Id 5 is for a 1-byte Vendor Defined INPUT/OUTPUT.
  - Report Id 6 is for a 2-byte Vendor Defined INPUT/OUTPUT.

## Installation & Usage

- Copy the .py file from this repository to the root of the CIRCUITPY folder.
- Copy the adafruit_hid and adafruit_ble libraries into the CIRCUITPY/lib folder.
- Pairing on macOS / Windows will start the HID communication.
- After OS pairing, open webhid_vendor_defined.html in Chrome, click "Connect HID Device," and connect the HID device to begin data communication.
  - Data will be received from CircuitPython.
  - After entering a number, clicking "Send 1 Byte" or "Send 2 Bytes" will send data to CircuitPython.
- It can simultaneously send Keyboard, Mouse, and Consumer Control data (currently commented out).
