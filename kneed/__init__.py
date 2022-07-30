from .data_generator import DataGenerator
from .knee_locator import KneeLocator
from .shape_detector import find_shape

with open("kneed/VERSION", mode='r', encoding="utf-8") as f:
    __version__ = f.readline()
