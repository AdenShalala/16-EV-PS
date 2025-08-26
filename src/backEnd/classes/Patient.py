from enum import Enum
from datetime import date
from dataclasses import dataclass

@dataclass
class Patient:
    first_name: str
    last_name: str
    height: float
    weight: float
    amputation_type: str
    socket_type: str
    email: str
    password: str
    patient_id: str
    clinician_id: str
    month_year_birth: date
    gender: str
    #Before the Enum is sorted out, a string will be used for the sake of immediate construction for testing.
    #amputation_type: Enum
    first_fitting: date
    hours_per_week: int
    distance_per_week: float
    activities: list