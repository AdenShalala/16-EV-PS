from enum import Enum
from dataclasses import dataclass

@dataclass
class Sensor:
    location: Enum
    type: str
    pressure_tolerance: float
    signal: list
    timestamp: list
    points_of_interest: list

