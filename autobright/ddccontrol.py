import re
import subprocess

from autobright.colorhugals import ColorHug
from autobright.core import Display
from autobright.measurements import Measurements


class DDCControl(Display):
    def __init__(self, device: int):
        self.device = device
        self.measurements = Measurements()
        self.sensor = ColorHug()

    def set_brightness(self, brightness: int) -> None:
        assert 0 <= brightness <= 100, "Brightness must be between 0 and 100."

        command = [
            "ddccontrol",
            "-r",
            "0x10",
            "-w",
            str(brightness),
            f"dev:/dev/i2c-{self.device}",
        ]
        status = subprocess.call(command)

        if status != 0:
            print("ddccontrol failed but it might still have worked")

    def get_brightness(self) -> int:
        command = [
            "ddccontrol",
            "-r",
            "0x10",
            f"dev:/dev/i2c-{self.device}",
        ]
        print(command)
        output = subprocess.run(command, check=True, capture_output=True)
        lines = output.stdout.decode().split("\n")
        for line in lines:
            print(line)
            if m := re.search(r"Control 0x10: \+/(\d+)/100 C", line):
                return int(m.group(1))
        raise RuntimeError("Could not read brightness from display.")
