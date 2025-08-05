from dataclasses import dataclass
from Patient import Patient

@dataclass
class Clinician:
    clinician_id: str       
    name: str              
    email: str            
    password: str      
    patients: list # The patients which this clinician can view
