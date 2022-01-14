from enum import Enum
import random
import string


class BaseEnum(Enum):
    @classmethod
    def get_choices(cls):
        return [(item.name, item.value) for item in cls]

    @classmethod
    def get_value(cls, name):
        value = [item.value for item in cls if item.name == name]
        if value:
            return value[0]

    @classmethod
    def get_values(cls):
        values = [item.value for item in cls]
        return values

    @classmethod
    def get_name(cls, value):
        name = [item.name for item in cls if item.value == value]
        if name:
            return name[0]


def random_str(n: int):
    return ''.join([random.choice(string.ascii_lowercase) for _ in range(n)])
