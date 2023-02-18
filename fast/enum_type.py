from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(type(Color.RED))
"""Output.
    <enum 'Color'>
"""

print(isinstance(Color.RED, Color))
print(Color.RED.name)
print(Color.RED.value)

"""Output.
    True.
    RED
    1
"""

print(Color.PURPLE in Color)