from autobright.core import BrightnessModel


class ProportionalBrightnessModel(BrightnessModel):
    def map(self, reading: float) -> float:
        b = 0.0211292e-3
        return min(b * reading, 1.0)
