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

@dataclass
class Session:
    session_id: str
    secret_hash: str
    created_at: datetime