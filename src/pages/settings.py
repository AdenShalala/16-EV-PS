
from nicegui import ui, app, events
import pages.utilities as utilities
import api
from functools import partial
from starlette.formparsers import MultiPartParser
import threading
import xml.etree.ElementTree as ET
from schema import *
import database
from uuid import uuid4
from faker import Faker

from tqdm import tqdm

MultiPartParser.spool_max_size = 1024 * 1024 * 5  

# ppc = patients_per_clinician
# spp = sensors_per_patient
# app = acivities_per_patient


def generate(admins: int, clinicians: int, ppc: int, spp: int, app: int, readings: bool):
    fake = Faker()
    xml = [
        "", "", ""
    ]

    xml[0] += '<?xml version="1.0" encoding="UTF-8"?>\n'
    # Generate admin user
    admin_id = uuid4()
    xml[0] += '<root>\n'


    for _ in range(admins):
        xml[0] += '\t<Admin>\n\t\t<admin_id>' + str(admin_id) + '</admin_id>'
        admin_first_name = fake.first_name()
        admin_last_name = fake.last_name()
        xml[0] += '\n\t\t<first_name>' + admin_first_name + '</first_name>'
        xml[0] += '\n\t\t<last_name>' + admin_last_name + '</last_name>'
        xml[0] += '\n\t\t<email>' + admin_first_name.lower() + '.' + admin_last_name.lower() + '@admin.com</email>'
        xml[0] += '\n\t\t<password>$argon2id$v=19$m=65536,t=3,p=4$FAFD4TpX4HPVRZjT/4NxtA$ehY7Wx6ZeKzLGt4sl62xZeIiRhvAuXkV3RAe5Pi/TaE</password>'
        xml[0] += '\n\t</Admin>'

    clinician_ids = []
    # Generate n Clinicians
    for _ in range(clinicians):
        clinician_id = uuid4()
        clinician_ids.append(str(clinician_id))
        xml[0] += '\n\t<Clinician>\n\t\t<clinician_id>' + str(clinician_id) + '</clinician_id>'
        clinician_first_name = fake.first_name()
        clinician_last_name = fake.last_name()
        xml[0] += '\n\t\t<first_name>' + clinician_first_name + '</first_name>'
        xml[0] += '\n\t\t<last_name>' + clinician_last_name + '</last_name>'
        xml[0] += '\n\t\t<email>' + clinician_first_name.lower() + '.' + clinician_last_name.lower() + '@clinician.com</email>'
        xml[0] += '\n\t\t<password>$argon2id$v=19$m=65536,t=3,p=4$FAFD4TpX4HPVRZjT/4NxtA$ehY7Wx6ZeKzLGt4sl62xZeIiRhvAuXkV3RAe5Pi/TaE</password>'
        xml[0] += '\n\t</Clinician>'

    patient_ids = []
    # Generate 8 Patients, 4 for each Clinician
    for clinician_id in clinician_ids:
        for _ in range(ppc):
            patient_id = uuid4()
            patient_ids.append(str(patient_id))
            xml[0] += '\n\t<Patient>\n\t\t<patient_id>' + str(patient_id) + '</patient_id>'
            patient_first_name = fake.first_name()
            patient_last_name = fake.last_name()
            xml[0] += '\n\t\t<first_name>' + patient_first_name + '</first_name>'
            xml[0] += '\n\t\t<last_name>' + patient_last_name + '</last_name>'
            xml[0] += '\n\t\t<height>' + str(fake.random_int(min=150, max=200)) + '</height>'
            xml[0] += '\n\t\t<weight>' + str(fake.random_int(min=50, max=120)) + '</weight>'
            xml[0] += '\n\t\t<amputation_type>' + fake.random_element(elements=('Below Knee', 'Above Knee', 'Below Elbow', 'Above Elbow')) + '</amputation_type>'
            xml[0] += '\n\t\t<prosthetic_type>' + fake.random_element(elements=('Carbon', 'Steel', 'Aluminium', 'Bionic')) + '</prosthetic_type>'
            xml[0] += '\n\t\t<email>' + patient_first_name.lower() + '.' + patient_last_name.lower() + '@patient.com</email>'
            xml[0] += '\n\t\t<password>$argon2id$v=19$m=65536,t=3,p=4$FAFD4TpX4HPVRZjT/4NxtA$ehY7Wx6ZeKzLGt4sl62xZeIiRhvAuXkV3RAe5Pi/TaE</password>'
            xml[0] += '\n\t\t<user_id>USER' + str(fake.random_int(min=5, max=15)) + '</user_id>'
            xml[0] += '\n\t\t<clinician_id>' + clinician_id + '</clinician_id>'
            xml[0] += '\n\t</Patient>'
    # Generate 16 Activities, 2 for each Patient
    activity_types = ['Walking', 'Running', 'Jumping', 'Swimming']
    activity_ids = {}
    activity_times = {}
    for patient_id in patient_ids:
        activity_ids[patient_id] = []
        activity_times[patient_id] = []
        for _ in range(app):
            activity_id = uuid4()
            activity_ids[patient_id].append(str(activity_id))
            activity_type = fake.random_element(elements=activity_types)
            xml[1] += '\n\t<Activity>\n\t\t<activity_id>' + str(activity_id) + '</activity_id>'
            xml[1] += '\n\t\t<activity_type>' + activity_type + '</activity_type>'
            start_time = int(fake.unix_time(start_datetime=datetime.fromtimestamp(1704067200), end_datetime=datetime.now()))
            end_time = start_time + fake.random_int(min=180, max=800)
            activity_times[patient_id].append((start_time, end_time))
            xml[1] += '\n\t\t<start_time>' + str(start_time) + '</start_time>'
            xml[1] += '\n\t\t<end_time>' + str(end_time) + '</end_time>'
            xml[1] += '\n\t\t<is_uploaded>TRUE</is_uploaded>'
            xml[1] += '\n\t\t<patient_id>' + patient_id + '</patient_id>'
            xml[1] += '\n\t</Activity>'

    # sensor_ids = {patient_id: []}
    sensor_ids = {}
    # Generate 16 Sensors, 2 for each Patient
    for patient_id in patient_ids:
        sensor_ids[patient_id] = []
        for _ in range(spp):
            sensor_id = uuid4()
            sensor_ids[patient_id].append(str(sensor_id))
            xml[1] += '\n\t<Sensor>\n\t\t<sensor_id>' + str(sensor_id) + '</sensor_id>'
            xml[1] += '\n\t\t<patient_id>' + patient_id + '</patient_id>'
            xml[1] += '\n\t\t<sensor_type>' + str(fake.random_int(min=0, max=1)) + '</sensor_type>'
            xml[1] += '\n\t\t<location_name>' + fake.random_element(elements=('upper', 'lower', 'left', 'right')) + '</location_name>'
            xml[1] += '\n\t\t<sensor_location_id>' + str(uuid4()) + '</sensor_location_id>'
            xml[1] += '\n\t\t<is_connected>TRUE</is_connected>'
            xml[1] += '\n\t</Sensor>'

    # Generate 2 Series' of Pressure Readings for each Activity
    if readings:
        for patient_num, (patient_id, activities) in enumerate(activity_ids.items()):
            for activitity_num, activity_id in enumerate(activities):
                for i in range(activitity_num + 1):
                    start_time, end_time = activity_times[patient_id][activitity_num]
                    reading_series_id = uuid4()
                    pressure_value = fake.random_int(min=0, max=100)
                    for timestamp in range(start_time, end_time + 1):
                        pressure_reading_id = uuid4()
                        xml[2] += '\n\t<PressureReading>\n\t\t<pressure_reading_id>' + str(pressure_reading_id) + '</pressure_reading_id>'
                        xml[2] += '\n\t\t<pressure_value>' + str(pressure_value) + '</pressure_value>'
                        pressure_value += fake.random_int(min=-45, max=45)
                        xml[2] += '\n\t\t<time>' + str(timestamp) + '</time>'
                        xml[2] += '\n\t\t<is_uploaded>TRUE</is_uploaded>'
                        xml[2] += '\n\t\t<reading_series_id>' + str(reading_series_id) + '</reading_series_id>'
                        xml[2] += '\n\t</PressureReading>'
                    xml[2] += '\n\t<ActivityReading>\n\t\t<activity_id>' + activity_id + '</activity_id>'
                    xml[2] += '\n\t\t<reading_series_id>' + str(reading_series_id) + '</reading_series_id>'
                    xml[2] += '\n\t\t<sensor_id>' + sensor_ids[patient_id][i] + '</sensor_id>'
                    xml[2] += '\n\t</ActivityReading>'           
    
    xml[2] += '\n</root>'

    return xml

def navigate_clinician(clinician):
    app.storage.user['selected_clinician'] = clinician.clinician_id
    ui.navigate.to("/clinician")

def create() -> None:
    @ui.page('/settings')
    def settings():
        app.storage.user['current_page'] = '/settings'
        ui.page_title('SocketFit Admin')
        utilities.header()
        left_drawer = utilities.admin_sidebar()
        utilities.arrow(left_drawer)

        with ui.row().classes(' w-full flex justify-center'):
            with ui.card().classes('w-1/2 justify-center items-center bg-[#F5F5F5] dark:bg-[#1d1d1d] border border-[#2C25B2] no-shadow'):
                ui.label("Generate XML").classes('font-bold text-xl dark:text-white')    

                with ui.grid(columns=7, rows=1).classes('w-full'):
                    admins = ui.number('Admins', value=0, min=0)
                    clinicians = ui.number('Clinicians', value=0, min=0)
                    patients = ui.number('Patients', value=0, min=0)
                    sensors = ui.number('Sensors', value=0, min=0)
                    activities = ui.number('Activities', value=0, min=0)
                    pressure_readings = ui.checkbox('Pressure Readings').classes('col-span-2')

                def generate_xml():
                    if int(patients.value) >= 1 and int(clinicians.value) < 1:
                        ui.notify('Clinicians must be greater than 1', color='red')
                        return

                    if int(sensors.value) >= 1 and int(patients.value) < 1:
                        ui.notify('Patients must be greater than 1', color='red')
                        return
                    
                    if int(activities.value) >= 1 and int(patients.value) < 1:
                        ui.notify('Patients must be greater than 1', color='red')
                        return
                    
                    

                    xml = generate(int(admins.value), int(clinicians.value), int(patients.value), int(sensors.value), int(activities.value))
                    ui.download.content(xml[0] + xml[1] + xml[2], 'generated_data.xml')

                ui.button('Download XML', color='#FFB030', on_click=lambda: generate_xml()).classes('text-white')

                ui.separator()

                ui.label("Upload XML").classes('font-bold text-xl dark:text-white')  
                

                async def handle_upload(e: events.UploadEventArguments):
                    x = e.content.read().decode('utf-8')
                    
                    def read_thread(x):
                        root = ET.fromstring(x)
                        value = 0
                        lenx = len(list(root))

                        with tqdm(total=len(list(root))) as pbar:
                            for item in root.findall('Admin'):
                                admin_id = item.find('admin_id').text
                                first_name = item.find('first_name').text
                                last_name = item.find('last_name').text
                                email = item.find('email').text
                                password = item.find('password').text

                                admin = Admin(admin_id, first_name, last_name, email, password)
                                database.write_admin(admin)
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)

                            for item in root.findall('Clinician'):
                                clinician_id = item.find('clinician_id').text
                                first_name = item.find('first_name').text
                                last_name = item.find('last_name').text
                                email = item.find('email').text
                                password = item.find('password').text

                                clinician = Clinician(clinician_id, first_name, last_name, email, password)
                                database.write_clinician(clinician)
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)

                            for item in root.findall('Patient'):
                                patient_id = item.find('patient_id').text
                                first_name = item.find('first_name').text
                                last_name = item.find('last_name').text
                                height = item.find('height').text
                                weight = item.find('weight').text
                                amputation_type = item.find('amputation_type').text
                                prosthetic_type = item.find('prosthetic_type').text

                                email = item.find('email').text
                                password = item.find('password').text
                                user_id = item.find('user_id').text
                                clinician_id = item.find('clinician_id').text

                                patient = Patient(patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password, user_id, clinician_id)
                                database.write_patient(patient)
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)

                            for item in root.findall('Activity'):
                                activity_id = item.find('activity_id').text
                                activity_type = item.find('activity_type').text
                                start_time = item.find('start_time').text
                                end_time = item.find('end_time').text
                                is_uploaded = item.find('is_uploaded').text
                                patient_id = item.find('patient_id').text

                                activity = Activity(activity_id, activity_type, start_time, end_time, bool(is_uploaded), patient_id)
                                database.write_activity(activity)
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)

                            for item in root.findall('Sensor'):
                                sensor_id = item.find('sensor_id').text
                                patient_id = item.find('patient_id').text
                                sensor_type = item.find('sensor_type').text
                                location_name = item.find('location_name').text
                                sensor_location_id = item.find('sensor_location_id').text
                                is_connected = item.find('is_connected').text

                                sensor = Sensor(sensor_id, patient_id, sensor_type, location_name, sensor_type, sensor_location_id, bool(is_connected))
                                database.write_sensor(sensor)
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)

                            for item in root.findall('PressureReading'):
                                pressure_reading_id = item.find('pressure_reading_id').text
                                pressure_value = item.find('pressure_value').text
                                time = item.find('time').text
                                is_uploaded = item.find('is_uploaded').text
                                reading_series_id = item.find('reading_series_id').text

                                pressure_reading = PressureReading(pressure_reading_id, pressure_value, time, bool(is_uploaded), reading_series_id)
                                database.write_pressure_reading(pressure_reading)   
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)

                            for item in root.findall('ActivityReading'):
                                activity_id = item.find('activity_id').text
                                reading_series_id = item.find('reading_series_id').text
                                sensor_id = item.find('sensor_id').text

                                activity_reading = ActivityReading(activity_id, reading_series_id, sensor_id)
                                database.write_activity_reading(activity_reading)    
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)
                                
                    thread = threading.Thread(target=read_thread, args=(x,))
                    thread.start()

                with ui.row().classes('w-full justify justify-center'):
                    ui.upload(on_upload=handle_upload, max_file_size=10_485_760).props('accept=.xml').classes('max-w-full flat').style('--q-primary: #FFB030')
                    progress_bar = ui.linear_progress(value=0, color="#FFB030", show_value=False).classes('w-2/3 rounded') 
                



            
