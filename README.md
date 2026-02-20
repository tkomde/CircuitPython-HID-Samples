# CircuitPython HID Samples

Various samples for HID.
Items that did not move are also listed.

## List of samples that worked

|Name|Detail|The board |Host OS |
|:--:|:--|:--|:--|
|Vendor Defined (BLE)|Performing INPUT/OUTPUT communication using a Vendor Defined Usage Page with Chrome's WebHID.|- Xiao nRF52840 Sense (CircuitPython 10.1.0-beta.1)<br/>- When tested on the Xiao ESP32S3 (CircuitPython 10.1.0-beta.1), it appears to crash during initialization with this descriptor|- Chrome: M142 (macOS / Windows)<br/>- ChromeOS does not work.|
| Gamepad (USB) | Simple gamepad, the code written within the standard library that is commented out. Data from the IMU emulating the stick's movement. | M5AtomS3  | -Windows<br/>- macOS |
| Gamepad Fullspec Test(USB) | A configuration similar to the Gamepad commonly sold. | M5AtomS3 | Descriptors are only tested |
| Call from smartphone (BLE) | When the board tilts, activate voice command (via consumer controll) and execute call (via keyboard). | Xiao nRF52840 Sense (CircuitPython 10.1.0-beta.1) | Pixel 10 (Android 16) |
| USB Host Mouse | Capture usb mouse data with CircuitPython | Raspberry Pi Pico 2 W | CircuitPython 10.1.1 |

## List of sample that didn't work

|Name|Detail|The board |Host OS |
|:--:|:--|:--|:--|
| Telephony device (BLE) | Telephony Devices(0x0B) usage is likely not supported by the host OS. | Xiao nRF52840 Sense(CircuitPython 10.1.0-beta.1) | Pixel 10 (Android 16)<br/>iPhone 16 Pro (iOS 26) |
| Telephony device (USB) | Telephony Devices(0x0B) usage is likely not supported by the host OS. | M5AtomS3(CircuitPython 10.1.0-beta.1) | Pixel 10 (Android 16)|

## Notes

Consumer Page is convenient for controll smartphone.
0xCD (Play/Pause): Answer the phone call
0xCF (Voice command): Launch Gemini/Siri
