from typing import List

import scipy.interpolate

from autobright.core import BrightnessModel


class ProportionalBrightnessModel(BrightnessModel):
    def map(self, reading: int) -> int:
        b = 0.0211292
        return int(min(b * reading, 100))


class SplineModel(BrightnessModel):
    def __init__(self, base_x: List[int], base_y: List[int]):
        self.interpolator = scipy.interpolate.interp1d(base_x, base_y, kind="quadratic")

    def map(self, reading: int) -> int:
        return self.interpolator(reading)
