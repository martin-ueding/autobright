import subprocess
import sys
import threading
import time
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from autobright.colorhugals import ColorHug
from autobright.config import TomlConfig
from autobright.ddccontrol import DDCControl
from autobright.measurements import Measurements
from autobright.models import SplineModel


class GuiState:
    def __init__(self):
        self.config = TomlConfig()
        self.displays = self.config.make_ddccontrol()
        self.measurements = Measurements()
        self.model = SplineModel()
        try:
            self.sensor = ColorHug()
        except subprocess.CalledProcessError:
            self.sensor = None
        self.thread = None

    def set_brightness(self, brightness: int) -> None:
        print(f"Setting brightness to {brightness}.")
        for display in self.displays:
            display.set_brightness(brightness)

    def store_brightness(self, brightness: int) -> None:
        if self.sensor is None:
            return
        print(f"Storing brightness to {brightness}.")
        reading = self.sensor.get_reading()
        print(f"Read {reading} from the sensor.")
        self.measurements.add_measurement(reading, brightness)

    def checkbox_changed(self, checked: bool) -> None:
        print(checked)
        if checked:
            self.thread = threading.Thread(target=self.auto)
            self.thread.start()
        else:
            self.thread = None

    def auto(self) -> None:
        myself = self.thread
        while self.thread is not None and self.thread is myself:
            print("Auto!")
            reading = self.sensor.get_reading()
            brightness = self.model.map(reading)
            for display in self.displays:
                display.set_brightness(brightness)
            time.sleep(5)
        print("Thread exists")


class Window(QWidget):
    def __init__(self, gui_state: GuiState):
        super().__init__()
        # self.resize(300, 300)
        self.setWindowTitle("Autobright")
        layout = QVBoxLayout()
        self.setLayout(layout)
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setMaximum(100)
        layout.addWidget(slider)
        label = QLabel()
        layout.addWidget(label)
        slider.valueChanged.connect(lambda value: label.setText(f"Target: {value}"))
        button = QPushButton("Set")
        layout.addWidget(button)
        button.clicked.connect(lambda: gui_state.set_brightness(slider.value()))
        button = QPushButton("Store measurement")
        layout.addWidget(button)
        button.clicked.connect(lambda: gui_state.store_brightness(slider.value()))
        checkbox = QCheckBox("Auto", self)
        checkbox.clicked.connect(gui_state.checkbox_changed)
        layout.addWidget(checkbox)


def set_value(value):
    print(value)


def main():
    app = QApplication(sys.argv)
    gui_state = GuiState()
    window = Window(gui_state)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
