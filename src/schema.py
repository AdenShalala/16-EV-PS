from dataclasses import dataclass
from datetime import datetime

@dataclass
class Clinician:
    clinician_id: str
    first_name: str
    last_name: str    
    email: str
    password: str
    created_at: datetime
    # patients: list # The patients which this clinician can view

# This is just for returning values
@dataclass
class PublicClinican:
    clinician_id: str
    first_name: str
    last_name: str    
    email: str
    created_at: datetime

@dataclass
class Session:
    session_id: str
    clinician_id: str
    secret_hash: str
    last_verified_at: datetime
    created_at: datetime