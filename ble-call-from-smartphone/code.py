import time
import struct
import board
import digitalio
import busio
import pwmio

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
# from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC


###############
# imu準備
###############
imupwr = digitalio.DigitalInOut(board.IMU_PWR)
imupwr.direction = digitalio.Direction.OUTPUT
imupwr.value = True
time.sleep(0.1)
imu_i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
sensor = LSM6DS3TRC(imu_i2c)

ledG = pwmio.PWMOut(board.LED_GREEN, frequency=800)
ledG.duty_cycle = 65535

hid = HIDService()

device_info = DeviceInfoService(software_revision=adafruit_ble.__version__,
                                manufacturer="Adafruit Industries")
advertisement = ProvideServicesAdvertisement(hid)
# Advertise as Generic Wearable Audio Device
# https://www.bluetooth.com/specifications/assigned-numbers/
advertisement.appearance = 0x0940
scan_response = Advertisement()
scan_response.complete_name = "CP_Telephony"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    print("advertising")
    ble.start_advertising(advertisement, scan_response)
else:
    print("already connected")
    print(ble.connections)

k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)
cc = ConsumerControl(hid.devices)

accZwa = 0
accZwaM1 = 0
waCoeff = 0.2
pressStartCnt = 0
pressing = False

while True:
    ite = 0
    while not ble.connected:
        pass

    print("Connected")

    while ble.connected:
        rawAccX, rawAccY, rawAccZ = sensor.acceleration
        # print("AccX:", rawAccX, "AccY:", rawAccY, "AccZ:", rawAccZ)
        accZwa = rawAccZ * waCoeff + accZwa * (1 - waCoeff)

        print("accZwa:", accZwa)
        if accZwa < -3 and accZwaM1 >= -3:
            if not pressing:
                print("Pressing Start")
                pressStartCnt = ite
                pressing = True

                cc.press(0xCF)  # Launch voice command
                time.sleep(0.1)
                cc.release()
                time.sleep(2)
                k.send(Keycode.TAB)  # Move focus to search box (tab x3)
                time.sleep(0.1)
                k.send(Keycode.TAB)
                time.sleep(0.1)
                k.send(Keycode.TAB)
                time.sleep(0.1)
                kl.write("call to xxx-xxxx-xxxx")  # tel someone
                time.sleep(1)
                k.send(Keycode.ENTER)

                ledG.duty_cycle = 0

        if accZwa >= -3 and accZwaM1 < -3:
            if pressing:
                pressing = False
                print("Power release")
                # cc.release()
                # kl.write("Hello World!")
                ledG.duty_cycle = 65535

        if (ite - pressStartCnt > 20) and pressing:
            print("Long presssed")
            pressing = False
            # cc.release()
            ledG.duty_cycle = 65535

        accZwaM1 = accZwa

        time.sleep(0.1)

        ite += 1

    ble.start_advertising(advertisement)
