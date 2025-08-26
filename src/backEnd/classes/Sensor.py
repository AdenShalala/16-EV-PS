from enum import Enum
from dataclasses import dataclass

@dataclass
class Sensor:
    location: str
    sensor_location_id: str
    type: str
    readings: list

