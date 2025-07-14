from SQL.SQL_read import read_patients_by_clinician_id
from src.Patient import Patient
from src.Activity import Activity
from src.Sensor import Sensor

patients = read_patients_by_clinician_id("CLIN402")

for patient in patients:
    print(f"Patient {patient.patient_id}\n\
          Birthdate: {patient.month_year_birth} Gender: {patient.gender}\n\
          Height: {patient.height} Weight: {patient.weight}\n\
          Amputation Type: {patient.amputation_type} First Fit: {patient.first_fitting}\n\
          Socket Type: {patient.socket_type} AVG Hpurs per week: {patient.hours_per_week}") 