import subprocess

from autobright.core import Sensor


class ColorHug(Sensor):
    def get_reading(self) -> float:
        command = ["colorhug-cmd", "set-multiplier", "20"]
        subprocess.check_call(command)

        command = ["colorhug-cmd", "set-color-select", "white"]
        subprocess.check_call(command)

        command = ["colorhug-cmd", "take-reading-raw"]
        output = subprocess.check_output(command).decode().strip()

        command = ["colorhug-cmd", "set-multiplier", "0"]
        subprocess.check_call(command)

        words = output.split()
        reading = float(words[1])
        return reading
