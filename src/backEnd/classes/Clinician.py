from dataclasses import dataclass
from typing import List
from Patient import Patient

@dataclass
class Clinician:
    clinician_id: str       
    name: str              
    email: str            
    password: str      
    patients: List[Patient] # The patients which this clinician can view
