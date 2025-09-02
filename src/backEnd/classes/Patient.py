from datetime import date
from dataclasses import dataclass

@dataclass
class Patient:
    first_name: str
    last_name: str
    height: float
    weight: float
    amputation_type: str
    prosthetic_type: str
    email: str
    patient_id: str
    clinician_id: str
    activities: list