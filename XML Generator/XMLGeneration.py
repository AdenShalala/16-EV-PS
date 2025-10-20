from tracemalloc import start
from uuid import uuid4
from faker import Faker
fake = Faker()

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
# Generate admin user
admin_id = uuid4()
xml += '<Admin>\n\t<admin_id>' + str(admin_id) + '<admin_id>'
admin_first_name = fake.first_name()
admin_last_name = fake.last_name()
xml += '\n\t<first_name>' + admin_first_name + '</first_name>'
xml += '\n\t<last_name>' + admin_last_name + '</last_name>'
xml += '\n\t<email>' + admin_first_name.lower() + '.' + admin_last_name.lower() + '@example.com</email>'
xml += '\n\t<password>$argon2id$v=19$m=65536,t=3,p=4$FAFD4TpX4HPVRZjT/4NxtA$ehY7Wx6ZeKzLGt4sl62xZeIiRhvAuXkV3RAe5Pi/TaE</password>'
xml += '\n</Admin>'

clinician_ids = []
# Generate 2 Clinicians
for _ in range(2):
    clinician_id = uuid4()
    clinician_ids.append(str(clinician_id))
    xml += '\n<Clinician>\n\t<clinician_id>' + str(clinician_id) + '</clinician_id>'
    clinician_first_name = fake.first_name()
    clinician_last_name = fake.last_name()
    xml += '\n\t<first_name>' + clinician_first_name + '</first_name>'
    xml += '\n\t<last_name>' + clinician_last_name + '</last_name>'
    xml += '\n\t<email>' + clinician_first_name.lower() + '.' + clinician_last_name.lower() + '@example.com</email>'
    xml += '\n\t<password>$argon2id$v=19$m=65536,t=3,p=4$FAFD4TpX4HPVRZjT/4NxtA$ehY7Wx6ZeKzLGt4sl62xZeIiRhvAuXkV3RAe5Pi/TaE</password>'
    xml += '\n</Clinician>'

patient_ids = []
# Generate 4 Patients, 2 for each Clinician
for clinician_id in clinician_ids:
    for _ in range(2):
        patient_id = uuid4()
        patient_ids.append(str(patient_id))
        xml += '\n<Patient>\n\t<patient_id>' + str(patient_id) + '</patient_id>'
        patient_first_name = fake.first_name()
        patient_last_name = fake.last_name()
        xml += '\n\t<first_name>' + patient_first_name + '</first_name>'
        xml += '\n\t<last_name>' + patient_last_name + '</last_name>'
        xml += '\n\t<height>' + str(fake.random_int(min=150, max=200)) + '</height>'
        xml += '\n\t<weight>' + str(fake.random_int(min=50, max=120)) + '</weight>'
        xml += '\n\t<amputation_type>' + fake.random_element(elements=('Below Knee', 'Above Knee', 'Below Elbow', 'Above Elbow')) + '</amputation_type>'
        xml += '\n\t<prosthetic_type>' + fake.random_element(elements=('Carbon', 'Steel', 'Aluminium', 'Bionic')) + '</prosthetic_type>'
        xml += '\n\t<email>' + patient_first_name.lower() + '.' + patient_last_name.lower() + '@example.com</email>'
        xml += '\n\t<password>$argon2id$v=19$m=65536,t=3,p=4$FAFD4TpX4HPVRZjT/4NxtA$ehY7Wx6ZeKzLGt4sl62xZeIiRhvAuXkV3RAe5Pi/TaE</password>'
        xml += '\n\t<user_id>' + str(uuid4()) + '</user_id>'
        xml += '\n\t<clinician_id>' + clinician_id + '</clinician_id>'
        xml += '\n</Patient>'
xml2 = ""
# Generate 8 Activities, 2 for each Patient
activity_types = ['Walking', 'Running', 'Jumping', 'Swimming']
activity_ids = []
activity_times = []
for patient_id in patient_ids:
    for _ in range(2):
        activity_id = uuid4()
        activity_ids.append(str(activity_id))
        activity_type = fake.random_element(elements=activity_types)
        xml2 += '\n<Activity>\n\t<activity_id>' + str(activity_id) + '</activity_id>'
        xml2 += '\n\t<activity_type>' + activity_type + '</activity_type>'
        start_time = int(fake.unix_time())
        end_time = start_time + fake.random_int(min=300, max=7200)
        activity_times.append((start_time, end_time))
        xml2 += '\n\t<start_time>' + str(start_time) + '</start_time>'
        xml2 += '\n\t<end_time>' + str(end_time) + '</end_time>'
        xml2 = '\n\t<is_uploaded>TRUE</is_uploaded>'
        xml2 += '\n\t<patient_id>' + patient_id + '</patient_id>'
        xml2 += '\n</Activity>'

sensor_ids = []
# Generate 8 Sensors, 2 for each Patient
for patient_id in patient_ids:
    for _ in range(2):
        sensor_id = uuid4()
        sensor_ids.append(str(sensor_id))
        xml2 += '\n<Sensor>\n\t<sensor_id>' + str(sensor_id) + '</sensor_id>'
        xml2 += '\n\t<patient_id>' + patient_id + '</patient_id>'
        xml2 += '\n\t<sensor_type>' + str(fake.random_int(min=0, max=2)) + '</sensor_type>'
        xml2 += '\n\t<location_name>' + fake.random_element(elements=('Upper', 'Lower', 'Left', 'Right')) + '</location_name>'
        xml2 += '\n\t<sensor_location_id>' + str(fake.random_int(min=0, max=5)) + '</sensor_location_id>'
        xml2 += '\n\t<is_connected>TRUE</is_connected>'
        xml2 += '\n</Sensor>'
xml3 = ""
# Generate 2 Series' of Pressure Readings for each Activity
for i in range(len(activity_ids)):
    start_time, end_time = activity_times[i]
    reading_series_id = uuid4()
    # Generate Pressure Readings every second
    pressure_value = fake.random_int(min=0, max=100)
    for timestamp in range(start_time, end_time + 1):
        pressure_reading_id = uuid4()
        xml3 += '\n<Pressure_Reading>\n\t<pressure_reading_id>' + str(pressure_reading_id) + '</pressure_reading_id>'
        xml3 += '\n\t<pressure_value>' + str(pressure_value) + '</pressure_value>'
        pressure_value += fake.random_int(min=-45, max=45)
        xml3 += '\n\t<time>' + str(timestamp) + '</time>'
        xml3 += '\n\t<is_uploaded>TRUE</is_uploaded>'
        xml3 += '\n\t<reading_series_id>' + str(reading_series_id) + '</reading_series_id>'
        xml3 += '\n</Pressure_Reading>'
    xml3 += '\n<ActivityReading>\n\t<activity_id>' + activity_ids[i] + '</activity_id>'
    xml3 += '\n\t<reading_series_id>' + str(reading_series_id) + '</reading_series_id>'
    xml3 += '\n\t<sensor_id>' + sensor_ids[i % len(sensor_ids)] + '</sensor_id>'
    xml3 += '\n</ActivityReading>'

# Write to XML file
with open('generated_data.xml', 'w') as file:
    file.write(xml)
    file.write(xml2)
    file.write(xml3)