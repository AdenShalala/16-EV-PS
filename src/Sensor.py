from enum import Enum
from dataclasses import dataclass

@dataclass
class Sensor:
    sensor_id: str
    #Until Enums are sorted, these will be stored as Strings for the sake of immediate construction.
    #location: Enum
    location: str
    type: str
    pressure_tolerance: float
    signal: list
    timestamp: list
    points_of_interest: list

