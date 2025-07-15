from datetime import datetime
from dataclasses import dataclass

@dataclass
class Activity:
    end_time: datetime
    start_time: datetime
    type: str
    sensors: list