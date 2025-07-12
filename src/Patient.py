from enum import Enum
from sqlite3 import Date
from dataclasses import dataclass

@dataclass
class Patient:
    clinician_id: str
    month_year_birth: Date
    gender: str
    height: float
    weight: float
    #Before the Enum is sorted out, a string will be used for the sake of immediate construction for testing.
    #amputation_type: Enum
    amputation_type: str
    socket_type: str
    first_fitting: Date
    hours_per_week: int
    distance_per_week: float
    activities: list