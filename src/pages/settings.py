
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
import random

from tqdm import tqdm

MultiPartParser.spool_max_size = 1024 * 1024 * 5  

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
                    
                    if bool(pressure_readings.value) == True and (int(activities.value) < 1 or int(patients.value) < 1):
                        ui.notify('Patients or activities be greater than 1', color='red')
                        return                        

                    def generate(admins: int, clinicians: int, patients: int, sensors: int, activities: int, pressure_readings: bool):         
                        fake = Faker()

                        Clinicians = []
                        Patients = []
                        Sensors = []
                        Activities = []

                        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n'
                        download_bar.value = 0

                        password = "$argon2id$v=19$m=65536,t=3,p=4$FAFD4TpX4HPVRZjT/4NxtA$ehY7Wx6ZeKzLGt4sl62xZeIiRhvAuXkV3RAe5Pi/TaE"
                        amputation_types = ('Below Knee', 'Above Knee', 'Below Elbow', 'Above Elbow')
                        socket_types = ('Carbon', 'Steel', 'Aluminium', 'Bionic')
                        sensor_locations = ('upper', 'lower', 'left', 'right')
                        activity_types = ('Walking', 'Running', 'Jumping', 'Swimming')

                        times = []
                        sensors_used = []

                        total_iterations = (admins + clinicians + patients + sensors + activities) - 1
                        for i in range(activities):
                            n = fake.random_int(1, sensors)
                            total_iterations += n
                            sensors_used.append(n)

                            start_time = int(fake.unix_time(start_datetime=datetime.fromtimestamp(1704067200), end_datetime=datetime.now()))
                            end_time = start_time + fake.random_int(min=90, max=480)
                            times.append([start_time, end_time])
                            for i in range(start_time, end_time + 1):
                                total_iterations += 1

                        value = 0
                        with tqdm(total=total_iterations) as pbar:
                            for i in range(admins):       
                                id = str(uuid4())
                                first_name = fake.first_name()
                                last_name = fake.last_name()
                                email = first_name.lower() + '.' + last_name.lower() + '@admin.com'


                                xml += database.get_admin_xml(Admin(id, first_name, last_name, email, password))

                                value += 1
                                pbar.update(1)
                                download_bar.value = value / total_iterations

                            for i in range(clinicians):       
                                id = str(uuid4())
                                first_name = fake.first_name()
                                last_name = fake.last_name()
                                email = first_name.lower() + '.' + last_name.lower() + '@clinician.com'
                                
                                clinician = Clinician(id, first_name, last_name, email, password)

                                xml += database.get_clinician_xml(clinician)

                                Clinicians.append(clinician)

                                value += 1
                                pbar.update(1)
                                download_bar.value = value / total_iterations

                            for clinician in Clinicians:
                                for i in range(patients):
                                    id = str(uuid4())
                                    first_name = fake.first_name()
                                    last_name = fake.last_name()
                                    email = first_name.lower() + '.' + last_name.lower() + '@patient.com'
                                    user_id = str(fake.random_int(min=5, max=15))
                                    height = str(fake.random_int(min=150, max=200))
                                    weight = str(fake.random_int(min=50, max=120))
                                    amputation_type = fake.random_element(elements=amputation_types)
                                    socket_type = fake.random_element(elements=socket_types)
                                    amputation_date = fake.date_between_dates(datetime.fromtimestamp(0), datetime.fromtimestamp(1640955600))
                                    prosthetic_fitting_date = fake.date_between_dates(amputation_date, datetime.fromtimestamp(1672491600))
                                    clinician_id = clinician.clinician_id

                                    patient = Patient(id, first_name, last_name, height, weight, amputation_type, socket_type, amputation_date, prosthetic_fitting_date, email, password, user_id, clinician_id)

                                    xml += database.get_patient_xml(patient)

                                    Patients.append(patient)

                                    value += 1
                                    pbar.update(1)          
                                    download_bar.value = value / total_iterations                          

                            for patient in Patients:
                                patient_id = patient.patient_id
                                for i in range(sensors):
                                    
                                    id = str(uuid4())
                                    sensor_type = str(fake.random_int(0, 1))
                                    sensor_location = fake.random_element(elements=sensor_locations)
                                    sensor_location_id = str(uuid4())

                                    sensor = Sensor(id, patient_id, sensor_type, sensor_location, sensor_type, sensor_location_id, True)

                                    xml += database.get_sensor_xml(sensor)

                                    Sensors.append(sensor)
                                    value += 1
                                    pbar.update(1)
                                    download_bar.value = value / total_iterations
                                
                                for i in range(activities):
                                    id = str(uuid4())
                                    activity_type = fake.random_element(elements=activity_types)
                                    start_time = times[i][0]
                                    end_time = times[i][1]

                                    activity = Activity(id, activity_type, start_time, end_time, True, patient_id)
                                
                                    xml += database.get_activity_xml(activity)

                                    Activities.append(activity)
                                    value += 1
                                    pbar.update(1)
                                    download_bar.value = value / total_iterations

                            if pressure_readings:
                                for i, activity in enumerate(Activities):  
                                    patient

                                    for x in Patients:
                                        if x.patient_id == activity.patient_id:
                                            patient = x
                                            break           

                                    patients_sensors = []

                                    for sensor in Sensors:
                                        if sensor.patient_id == patient.patient_id:
                                            patients_sensors.append(sensor)

                                    
                                    n = sensors_used[max(0, min(i - 1, sensors))]
                                    
                                    for j in range(n):
                                        sensor = patients_sensors[j]
                                        start_time, end_time = activity.start_time, activity.end_time
                                        id = str(uuid4())

                                        xml += database.get_activity_reading_xml(ActivityReading(activity.activity_id, id, sensor.sensor_id))

                                        pressure_value = fake.random_int(-100, 100)
                                        for timestamp in range(start_time, end_time + 1):
                                            pressure_reading_id = str(uuid4())
                                            
                                            # Add occasional spikes/drops (10% chance)
                                            if random.random() < 0.1:
                                                change = fake.pyfloat(min_value=-15, max_value=15)
                                            else:
                                                change = fake.pyfloat(min_value=-5, max_value=5)
                                            
                                            pressure_value = max(-35, min(75, pressure_value + change))

                                            xml += database.get_pressure_reading_xml(PressureReading(pressure_reading_id, pressure_value, timestamp, True, id))

                                            value += 1
                                            pbar.update(1)    
                                            download_bar.value = value / total_iterations

                                    value += 1
                                    pbar.update(1)
                                    download_bar.value = value / total_iterations

                        xml += '\n</root>'                 


                        ui.download.content(xml, 'generated_data.xml')       

                    generate(int(admins.value), int(clinicians.value), int(patients.value), int(sensors.value), int(activities.value), bool(pressure_readings.value))           

                ui.button('Download XML', color='#FFB030', on_click=lambda: generate_xml()).classes('text-white')
                download_bar = ui.linear_progress(value=0, color="#FFB030", show_value=False).classes('w-full rounded') 
                ui.separator()

                ui.label("Upload XML").classes('font-bold text-xl dark:text-white')  
                

                async def handle_upload(e: events.UploadEventArguments):
                    x = e.content.read().decode('utf-8')
                    
                    def read_thread(x):
                        root = ET.fromstring(x)
                        value = 0
                        lenx = len(list(root))

                        with tqdm(total=len(list(root))) as pbar:
                            for item in root.findall('Session'):
                                id = item.find('id').text
                                account_type = item.find('account_type').text
                                secret_hash = item.find('secret_hash').text
                                created_at = item.find('created_at').text
                                last_verified_at = item.find('last_verified_at').text

                                session = Session(id, account_type, secret_hash, created_at, last_verified_at)
                                database.write_session(session)
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)

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
                                socket_type = item.find('socket_type').text
                                amputation_date = item.find('amputation_date').text
                                prosthetic_fitting_date = item.find('prosthetic_fitting_date').text

                                email = item.find('email').text
                                password = item.find('password').text
                                user_id = item.find('user_id').text
                                clinician_id = item.find('clinician_id').text

                                patient = Patient(patient_id, first_name, last_name, height, weight, amputation_type, socket_type, amputation_date, prosthetic_fitting_date, email, password, user_id, clinician_id)
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

                            connection = database.get_database()
                            cursor = connection.cursor()
                            
                            items = []

                            for item in root.findall('PressureReading'):
                                pressure_reading_id = item.find('pressure_reading_id').text
                                pressure_value = item.find('pressure_value').text
                                time = item.find('time').text
                                is_uploaded = item.find('is_uploaded').text
                                reading_series_id = item.find('reading_series_id').text

                                #pressure_reading = PressureReading(pressure_reading_id, pressure_value, time, bool(is_uploaded), reading_series_id)
                                ##database.write_pressure_reading(pressure_reading)   
                                items.append((pressure_reading_id, pressure_value, time, bool(is_uploaded), reading_series_id))
                                value += 1
                                progress_bar.value = value / lenx
                                pbar.update(1)

                            cursor.executemany("INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, is_uploaded, reading_series_id) VALUES (%s, %s, %s, %s, %s)", items)
                            connection.commit()
                            connection.close()

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
                    ui.upload(on_upload=handle_upload, max_file_size=104857600).props('accept=.xml').classes('max-w-full flat').style('--q-primary: #FFB030')
                    progress_bar = ui.linear_progress(value=0, color="#FFB030", show_value=False).classes('w-full rounded') 
                
                ui.separator()
                ui.label("Export Database as XML").classes('font-bold text-xl dark:text-white')  

                def export():
                    sessions = database.get_sessions()
                    admins = database.get_admins()
                    clinicians = database.get_clinicians()
                    patients = database.get_patients()
                    sensors = database.get_sensors()
                    activities = database.get_activities()
                    activity_readings = database.get_activity_readings()
                    pressure_readings = database.get_pressure_readings()


                    total_iterations = len(sessions) + len(admins) + len(clinicians) + len(patients) + len(sensors) + len(activities) + len(activity_readings) + len(pressure_readings)

                    value = 0
                    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n'
                    with tqdm(total=total_iterations) as pbar:
                        for session in sessions:
                            xml += database.get_session_xml(session)
                            value += 1
                            pbar.update(1)
                            export_bar.value = value / total_iterations                                

                        for admin in admins:
                            xml += database.get_admin_xml(admin)
                            value += 1
                            pbar.update(1)
                            export_bar.value = value / total_iterations                            

                        for clinician in clinicians:
                            xml += database.get_clinician_xml(clinician)
                            value += 1
                            pbar.update(1)
                            export_bar.value = value / total_iterations     

                        for patient in patients:
                            xml += database.get_patient_xml(patient)
                            value += 1
                            pbar.update(1)
                            export_bar.value = value / total_iterations     

                        for sensor in sensors:
                            xml += database.get_sensor_xml(sensor)
                            value += 1
                            pbar.update(1)
                            export_bar.value = value / total_iterations  

                        for activity in activities:
                            xml += database.get_activity_xml(activity)
                            value += 1
                            pbar.update(1)
                            export_bar.value = value / total_iterations  

                        for activity_reading in activity_readings:
                            xml += database.get_activity_reading_xml(activity_reading)
                            value += 1
                            pbar.update(1)
                            export_bar.value = value / total_iterations  

                        for pressure_reading in pressure_readings:
                            xml += database.get_pressure_reading_xml(pressure_reading)
                            value += 1
                            pbar.update(1)
                            export_bar.value = value / total_iterations  

                    xml += '\n</root>'                 
                    ui.download.content(xml, 'export.xml')   


                with ui.row().classes('w-full justify justify-center'):
                    ui.button('Export Database', color='#FFB030', on_click=lambda: export()).classes('text-white')
                    export_bar = ui.linear_progress(value=0, color="#FFB030", show_value=False).classes('w-full rounded') 

            
