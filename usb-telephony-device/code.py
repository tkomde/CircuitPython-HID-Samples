import time
import struct
import usb_hid
import board
import math
import busio
import digitalio
from adafruit_hid import find_device


class Telephony:
    def __init__(self, devices):
        self._telephony_device = find_device(devices, usage_page=0x0B, usage=0x05)

        self._report = bytearray(1)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(1)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(
                button) - 1
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(
                1 << self._validate_button_number(button) - 1)
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""

        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        struct.pack_into(
            "B",
            self._report,
            0,
            self._buttons_state,
        )

        if always or self._last_report != self._report:
            print("reporting!!!", self._report)
            self._telephony_device.send_report(self._report, 1)
            # Remember what we sent, without allocating new storage.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 16:
            raise ValueError("Button number must in range 1 to 16")
        return button

tp = Telephony(usb_hid.devices)
button = digitalio.DigitalInOut(board.BTN)
button.pull = digitalio.Pull.UP

print("Loop start ")

i = 0

while True:
    i += 1

    # 50Hz
    if (i % 2 == 0):
        if button.value:
            #print("Button released")
            tp.release_buttons(1)
        else:
            tp.press_buttons(1)

    time.sleep(0.01)
