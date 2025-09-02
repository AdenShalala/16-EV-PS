from datetime import datetime
from dataclasses import dataclass

@dataclass
class Activity:
    type: str
    start_time: datetime
    end_time: datetime
    activity_id: str
    sensors: list