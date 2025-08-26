from dataclasses import dataclass

@dataclass
class PressureReading:
    pressure_value: float
    time: int
    sensor_type: int