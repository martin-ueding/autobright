import abc


class Sensor(abc.ABC):
    def get_reading(self) -> int:
        raise NotImplementedError()


class BrightnessModel(abc.ABC):
    def map(self, reading: int) -> int:
        raise NotImplementedError()


class Display(abc.ABC):
    def set_brightness(self, brightness: int) -> None:
        raise NotImplementedError()

    def get_brightness(self) -> int:
        raise NotImplementedError()
