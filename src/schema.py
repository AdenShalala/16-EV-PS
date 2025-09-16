from dataclasses import dataclass
from datetime import datetime

@dataclass
class Clinician:
    clinician_id: str
    first_name: str
    last_name: str    
    email: str
    password: str
    # patients: list # The patients which this clinician can view

