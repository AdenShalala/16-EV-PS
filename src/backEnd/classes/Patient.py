from enum import Enum
from datetime import date
from dataclasses import dataclass

@dataclass
class Patient:
    patient_id: str
    clinician_id: str
    month_year_birth: date
    gender: str
    height: float
    weight: float
    #Before the Enum is sorted out, a string will be used for the sake of immediate construction for testing.
    #amputation_type: Enum
    amputation_type: str
    socket_type: str
    first_fitting: date
    hours_per_week: int
    distance_per_week: float
    activities: list