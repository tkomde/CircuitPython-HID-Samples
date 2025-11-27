import time
import struct
import usb_hid
import board
import math
import busio
import digitalio
import mpu6886
from adafruit_hid import find_device


class Gamepad:
    """Emulate a generic gamepad controller with 16 buttons,
    numbered 1-16, and two joysticks, one controlling
    ``x` and ``y`` values, and the other controlling ``z`` and
    ``r_z`` (z rotation or ``Rz``) values.

    The joystick values could be interpreted
    differently by the receiving program: those are just the names used here.
    The joystick values are in the range -127 to 127."""

    def __init__(self, devices):
        """Create a Gamepad object that will send USB gamepad HID reports.

        Devices can be a list of devices that includes a gamepad device or a gamepad device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)

        # Reuse this bytearray to send mouse reports.
        # Typically controllers start numbering buttons at 1 rather than 0.
        # report[0] buttons 1-8 (LSB is button 1)
        # report[1] buttons 9-16
        # report[2] joystick 0 x: -127 to 127
        # report[3] joystick 0 y: -127 to 127
        # report[4] joystick 1 x: -127 to 127
        # report[5] joystick 1 y: -127 to 127
        self._report = bytearray(8)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(8)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_rx = 0
        self._joy_ry = 0
        self._joy_hat = 0

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

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

    def move_joysticks(self, x=None, y=None, z=None, rx=None, ry=None, hat=None):
        """Set and send the given joystick values.
        The joysticks will remain set with the given values until changed

        One joystick provides ``x`` and ``y`` values,
        and the other provides ``z`` and ``r_z`` (z rotation).
        Any values left as ``None`` will not be changed.

        All values must be in the range -127 to 127 inclusive.

        Examples::

            # Change x and y values only.
            gp.move_joysticks(x=100, y=-50)

            # Reset all joystick values to center position.
            gp.move_joysticks(0, 0, 0, 0)
        """
        if x is not None:
            self._joy_x = self._validate_joystick_value(x)
        if y is not None:
            self._joy_y = self._validate_joystick_value(y)
        if z is not None:
            self._joy_z = self._validate_joystick_value(z)
        if rx is not None:
            self._joy_rx = self._validate_joystick_value(rx)
        if ry is not None:
            self._joy_ry = self._validate_joystick_value(ry)
        if hat is not None:
            self._joy_hat = self._validate_joystick_value(hat)
        self._send()

    def reset_all(self):
        """Release all buttons and set joysticks to zero."""
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_rx = 0
        self._joy_ry = 0
        self._joy_hat = 0
        self._send(always=True)

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        struct.pack_into(
            "<bbbbbbH",
            self._report,
            0,
            self._joy_x,
            self._joy_y,
            self._joy_z,
            self._joy_rx,
            self._joy_ry,
            self._joy_hat,
            self._buttons_state,
        )

        if always or self._last_report != self._report:
            print("reporting!!!")
            self._gamepad_device.send_report(self._report)
            # Remember what we sent, without allocating new storage.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 16:
            raise ValueError("Button number must in range 1 to 16")
        return button

    @staticmethod
    def _validate_joystick_value(value):
        if not -127 <= value <= 127:
            raise ValueError("Joystick value must be in range -127 to 127")
        return value


gp = Gamepad(usb_hid.devices)

i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
sensor = mpu6886.MPU6886(i2c)

button = digitalio.DigitalInOut(board.BTN)
button.pull = digitalio.Pull.UP

# Equivalent of Arduino's map() function.


def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


print("Loop start ")
oylerX = 0
oylerZ = 0
i = 0

while True:
    # rawAccX, rawAccY, rawAccZ = sensor.acceleration
    rawGyroX, rawGyroY, rawGyroZ = sensor.gyro
    gyroX = rawGyroX + 0.0156  # drift calib
    oylerX += gyroX
    gyroZ = rawGyroZ + 0.0156  # drift calib
    oylerZ += gyroZ

    if (not -50 < oylerX < 50):
        oylerX = 0
    if (not -50 < oylerZ < 50):
        oylerZ = 0

    i += 1

    # 50Hz
    if (i % 2 == 0):

        if button.value:
            gp.release_buttons(1)
        else:
            gp.press_buttons(1)
            oylerX = 0
            oylerZ = 0

        # Pass only oylerZ is not,,
        finalOylerX = -1 * oylerX if (not -6 < oylerX < 6) else 0
        finalOylerZ = -1 * oylerZ if (not -6 < oylerZ < 6) else 0
        # Convert range[0, 65535] to -127 to 127
        gp.move_joysticks(
            x=round(range_map(finalOylerZ, -50, 50, -127, 127)),
            y=round(range_map(finalOylerX, -50, 50, -127, 127)),
        )

    if (i % 20 == 0):
        print(f"{oylerZ:.1f} {oylerX:.1f} {not button.value}")

    time.sleep(0.01)
