import dataclasses
from enum import Enum


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args,
                                                                     **kwargs)
        return cls._instances[cls]


def dicts_to_dataclasses(instance):
    """Convert all fields of type `dataclass` into an instance of the
    specified data class if the current value is of type dict."""
    cls = type(instance)
    for f in dataclasses.fields(cls):
        if dataclasses.is_dataclass(f.type):

            value = getattr(instance, f.name)
            if not isinstance(value, dict):
                continue

            new_value = f.type(**value)
            setattr(instance, f.name, new_value)
        try:
            if issubclass(f.type, Enum):
                value = getattr(instance, f.name)
                if not isinstance(value, str):
                    continue

                new_value = f.type(value)
                setattr(instance, f.name, new_value)
        except TypeError:
            pass