import click

from autobright.colorhugals import ColorHug
from autobright.ddccontrol import DDCControl
from autobright.measurements import Measurements
from autobright.models import ProportionalBrightnessModel


@click.group()
def main():
    pass


@main.command()
def adjust() -> None:
    sensor = ColorHug()
    display = DDCControl(7)
    model = ProportionalBrightnessModel()

    reading = sensor.get_reading()
    brightness = model.map(reading)
    display.set_brightness(brightness)


@main.command()
def read() -> None:
    sensor = ColorHug()
    for i in range(10):
        reading = sensor.get_reading()
        print(reading)


@main.command()
def measure() -> None:
    sensor = ColorHug()
    display = DDCControl(9)
    measurements = Measurements()

    brightness = display.get_brightness()
    reading = sensor.get_reading()
    print(f'Brightness: {brightness}, Reading: {reading}')
    measurements.add_measurement(reading, brightness)


@main.command()
def web_ui() -> None:
    from autobright.webui import main as webui_main

    webui_main()


if __name__ == "__main__":
    main()
