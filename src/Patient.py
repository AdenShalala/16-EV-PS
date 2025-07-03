from enum import Enum
from sqlite3 import Date
from dataclasses import dataclass

@dataclass
class User:
    clinician_id: str
    month_year_birth: Date
    gender: str
    height: float
    weight: float
    amputation_type: Enum
    socket_type: str
    first_fitting: Date
    hours_per_week: int
    distance_per_week: float
    activities: list