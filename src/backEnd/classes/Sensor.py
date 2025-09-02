from dataclasses import dataclass

@dataclass
class Sensor:
    sensor_id: str
    location: str
    sensor_location_id: str
    type: str
    readings: list