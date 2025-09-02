from dataclasses import dataclass

@dataclass
class PressureReading:
    pressure_value: float
    time: int
    sensor_type: int
    pressure_reading_id: str
    activity_id: str
    sensor_id: str