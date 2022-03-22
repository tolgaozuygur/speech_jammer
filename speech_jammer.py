from evdev import InputDevice, categorize, ecodes
import evdev
import time
import subprocess
import random
from select import select
import RPi.GPIO as GPIO


def main():
    print("Starting...")

    # config
    # change the device name and button codes to match your controller.
    # You can learn these values by using the Evdev library.
    btDeviceName = "MOCUTE-051_A30-1986"
    silenceBtn = 305
    safeShutdownBtn1 = 308
    safeShutdownBtn2 = 304
    delayMin = 180000
    delayMax = 220000

    shutdownBtnHoldSec = 5
    statusLedPin = 17

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(statusLedPin, GPIO.OUT)
    connectToController()


def connectToController():
    btDevicePath = ""
    while btDevicePath == "":
        print("Waiting for bt device to connect...")
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.name == btDeviceName:
                btDevicePath = device.path
                print("Bt controller connected!")
        GPIO.output(statusLedPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(statusLedPin, GPIO.LOW)
        time.sleep(0.5)
    runDaf(btDevicePath)


def runDaf(btDevicePath):
    print("DAF Service started.")
    gamepad = InputDevice(btDevicePath)
    random.seed()
    silencerActive = 0
    shutdownBtn1Timer = 0
    shutdownBtn2Timer = 0
    try:
        while True:
            r, _, _ = select([gamepad], [], [], 0.1)
            if r:
                for event in gamepad.read():
                    if event.type == ecodes.EV_KEY:
                        if event.value == 1:
                            if event.code == silenceBtn:
                                if silencerActive == 0:
                                    # randomize delay each time it's activated
                                    randomDelay = random.randint(delayMin, delayMax)
                                    alsaProcess = subprocess.Popen(
                                        [
                                            "alsaloop",
                                            "-C",
                                            "hw:1,0",
                                            "-c",
                                            "1",
                                            "-P",
                                            "plughw:1,0",
                                            "-t",
                                            randomDelay,
                                        ]
                                    )
                                    GPIO.output(statusLedPin, GPIO.HIGH)
                                    silencerActive = 1
                                    print(f"Silencer enabled ({randomDelay})")
                                else:
                                    alsaProcess.terminate()
                                    GPIO.output(statusLedPin, GPIO.LOW)
                                    silencerActive = 0
                                    print("Silencer disabled")
                            elif event.code == safeShutdownBtn1:
                                print("Shutdown1 down")
                                shutdownBtn1Timer = time.time()
                            elif event.code == safeShutdownBtn2:
                                print("Shutdown2 down")
                                shutdownBtn2Timer = time.time()
                        if event.value == 0:
                            if event.code == safeShutdownBtn1:
                                print("Shutdown1 up")
                                shutdownBtn1Timer = 0
                            elif event.code == safeShutdownBtn2:
                                print("Shutdown2 up")
                                shutdownBtn2Timer = 0
            if shutdownBtn1Timer != 0 and shutdownBtn2Timer != 0:
                if (shutdownBtn1Timer + shutdownBtnHoldSec) < time.time() and (
                    shutdownBtn2Timer + shutdownBtnHoldSec
                ) < time.time():
                    print("Shutting down!")
                    # flash the led to indicate shutdown
                    shutdownBtn1Timer = 0
                    shutdownBtn2Timer = 0
                    for i in range(6):
                        GPIO.output(statusLedPin, GPIO.HIGH)
                        time.sleep(0.1)
                        GPIO.output(statusLedPin, GPIO.LOW)
                        time.sleep(0.1)
                    subprocess.call("sudo shutdown -h now", shell=True)
    except Exception as e:
        print(str(e))
        print("Controller disconnected.")
        if silencerActive == 1:
            GPIO.output(statusLedPin, GPIO.LOW)
            alsaProcess.terminate()
            silencerActive = 0
        connectToController()


if __name__ == "__main__":
    main()
