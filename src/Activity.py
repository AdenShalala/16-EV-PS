from click import DateTime
from dataclasses import dataclass

@dataclass
class Activity:
    end_time: DateTime
    start_time: DateTime
    type: str
    sensors: list