import subprocess
import time

from autobright.core import Sensor


class ColorHug(Sensor):
    def __init__(self):
        self.init()

    def init(self):
        command = ["colorhug-cmd", "boot-flash"]
        subprocess.run(command)
        time.sleep(0.03)

        command = ["colorhug-cmd", "set-multiplier", "20"]
        subprocess.run(command, check=True)
        time.sleep(0.03)

        command = ["colorhug-cmd", "set-color-select", "white"]
        subprocess.run(command, check=True)
        time.sleep(0.03)

    def get_reading(self) -> int:
        reading = None
        while not reading:
            command = ["colorhug-cmd", "take-reading-raw"]
            output = subprocess.check_output(command).decode().strip()
            time.sleep(0.03)
            words = output.split()
            reading = int(words[1])
        return reading

    def shutdown(self):
        command = ["colorhug-cmd", "set-multiplier", "0"]
        subprocess.run(command)
        time.sleep(0.03)

