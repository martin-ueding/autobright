import abc

class Sensor(abc.ABC):
    @abc.abstractmethod
    def get_reading(self) -> float:
        raise NotImplementedError()

class Mapping(abc.ABC):
    @abc.abstractmethod
    def map(self, reading: float) -> float:
        raise NotImplementedError()

class Display(abc.ABC):
    @abc.abstractmethod
    def set_brightness(self, percent: float) -> None:
        raise NotImplementedError()
