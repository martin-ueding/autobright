import sys
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from autobright.ddccontrol import DDCControl


class GuiState:
    def __init__(self):
        pass

    def set_device(self, devices: List[int]) -> None:
        print(f"Setting displays to {devices}.")
        self.displays = [DDCControl(device) for device in devices]

    def set_brightness(self, brightness: int) -> None:
        print(f"Setting brightness to {brightness}.")
        for display in self.displays:
            display.set_brightness(brightness)


class Window(QWidget):
    def __init__(self, gui_state: GuiState):
        super().__init__()
        # self.resize(300, 300)
        self.setWindowTitle("Autobright")
        layout = QVBoxLayout()
        self.setLayout(layout)
        line_edit = QLineEdit()
        line_edit.editingFinished.connect(
            lambda: gui_state.set_device([int(x) for x in line_edit.text().split()])
        )
        layout.addWidget(line_edit)
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setMaximum(100)
        layout.addWidget(slider)
        label = QLabel()
        layout.addWidget(label)
        slider.valueChanged.connect(lambda value: label.setText(f"Target: {value}"))
        button = QPushButton("Set")
        layout.addWidget(button)
        button.clicked.connect(lambda: gui_state.set_brightness(slider.value()))


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
