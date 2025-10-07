from dataclasses import dataclass
from datetime import datetime

@dataclass
class Session:
    session_id: str
    id: str
    account_type: str
    secret_hash: str
    last_verified_at: datetime
    created_at: datetime

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
class ActivityReading:
    activity_id: str
    reading_series_id: str
    sensor_id: str

@dataclass
class Sensor:
    sensor_id: str
    location_name: str
    sensor_location_id: str
    sensor_type: int
    is_connected: bool
    patient_email: str
    location_id: int
    pressure_sensor_id: str
    activity_id: str

@dataclass
class PressureReading:
    pressure_reading_id: str
    pressure_value: float
    time: int
    sensor_type: int
    is_uploaded: bool
    reading_series_id: str
    activity_id: str
    sensor_id: str

# This is just for returning values
@dataclass
class PublicClinican:
    clinician_id: str
    first_name: str
    last_name: str    
    email: str
    created_at: datetime
