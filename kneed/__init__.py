import pkgutil

from .data_generator import DataGenerator
from .knee_locator import KneeLocator
from .shape_detector import find_shape

__version__ = pkgutil.get_data(__name__, "VERSION").decode("utf-8").strip()
