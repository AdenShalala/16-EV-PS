from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
    session_id: str
    id: str
    account_type: str
    secret_hash: str
    created_at: datetime
    last_verified_at: datetime

@dataclass
class Admin:
    admin_id: str
    first_name: str
    last_name: str
    email: str
    password: str

@dataclass
class Clinician:
    clinician_id: str
    first_name: str
    last_name: str    
    email: str
    password: str
    created_at: datetime

@dataclass
class Patient:
    patient_id: str
    first_name: str
    last_name: str
    height: str
    weight: str
    amputation_type: str
    prosthetic_type: str
    email: str
    password: str
    # legacy
    user_id: str
    clinician_id: str

@dataclass
class Activity:
    activity_id: str
    activity_type: str
    start_time: int
    end_time: int
    is_uploaded: bool
    patient_id: str

@dataclass
class Sensor:
    sensor_id: str
    patient_id: str
    sensor_type: int
    location_name: str
    location_id: int
    sensor_location_id: str
    is_connected: bool

@dataclass
class PressureReading:
    pressure_reading_id: str
    pressure_value: float
    time: int
    is_uploaded: bool
    reading_series_id: str

@dataclass
class ActivityReading:
    activity_id: str
    reading_series_id: str
    sensor_id: str

# This is just for returning values
@dataclass
class PublicClinican:
    clinician_id: str
    first_name: str
    last_name: str    
    email: str
    created_at: datetime
