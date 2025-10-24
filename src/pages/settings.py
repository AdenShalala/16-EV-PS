
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
                        prosthetic_types = ('Carbon', 'Steel', 'Aluminium', 'Bionic')
                        sensor_locations = ('upper', 'lower', 'left', 'right')
                        activity_types = ('Walking', 'Running', 'Jumping', 'Swimming')

                        times = []

                        total_iterations = (admins + clinicians + patients + sensors + activities) - 1
                        for i in range(activities):
                            start_time = int(fake.unix_time(start_datetime=datetime.fromtimestamp(1704067200), end_datetime=datetime.now()))
                            end_time = start_time + fake.random_int(min=180, max=800)
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

                                xml += '\t<Admin>\n\t\t<admin_id>' + id + '</admin_id>'
                                xml += '\n\t\t<first_name>' + first_name + '</first_name>'
                                xml += '\n\t\t<last_name>' + last_name + '</last_name>'
                                xml += '\n\t\t<email>' + email + '</email>'
                                xml += '\n\t\t<password>' + password + '</password>'
                                xml += '\n\t</Admin>'

                                value += 1
                                pbar.update(1)
                                download_bar.value = value / total_iterations

                            for i in range(clinicians):       
                                id = str(uuid4())
                                first_name = fake.first_name()
                                last_name = fake.last_name()
                                email = first_name.lower() + '.' + last_name.lower() + '@clinician.com'
                                
                                clinician = Clinician(id, first_name, last_name, email, password)

                                xml += '\n\t<Clinician>\n\t\t<clinician_id>' + id + '</clinician_id>'
                                xml += '\n\t\t<first_name>' + first_name + '</first_name>'
                                xml += '\n\t\t<last_name>' + last_name + '</last_name>'
                                xml += '\n\t\t<email>' + email + '</email>'
                                xml += '\n\t\t<password>' + password + '</password>'
                                xml += '\n\t</Clinician>'

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
                                    prosthetic_type = fake.random_element(elements=prosthetic_types)
                                    clinician_id = clinician.clinician_id

                                    patient = Patient(id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password, user_id, clinician_id)

                                    xml += '\n\t<Patient>\n\t\t<patient_id>' + id + '</patient_id>'
                                    xml += '\n\t\t<first_name>' + first_name + '</first_name>'
                                    xml += '\n\t\t<last_name>' + last_name + '</last_name>'
                                    xml += '\n\t\t<height>' + height + '</height>'
                                    xml += '\n\t\t<weight>' + weight + '</weight>'
                                    xml += '\n\t\t<amputation_type>' + amputation_type + '</amputation_type>'
                                    xml += '\n\t\t<prosthetic_type>' + prosthetic_type + '</prosthetic_type>'
                                    xml += '\n\t\t<email>' + email + '</email>'
                                    xml += '\n\t\t<password>' + password + '</password>'
                                    xml += '\n\t\t<user_id>USER' + user_id + '</user_id>'
                                    xml += '\n\t\t<clinician_id>' + clinician_id + '</clinician_id>'
                                    xml += '\n\t</Patient>'

                                    Patients.append(patient)

                                    value += 1
                                    pbar.update(1)          
                                    download_bar.value = value / total_iterations                          

                            for patient in Patients:
                                patient_id = patient.patient_id
                                for i in range(sensors):
                                    
                                    id = str(uuid4())
                                    sensor_type = str(uuid4())
                                    sensor_location = fake.random_element(elements=sensor_locations)
                                    sensor_location_id = str(uuid4())

                                    sensor = Sensor(id, patient_id, sensor_type, sensor_location, sensor_type, sensor_location_id, True)

                                    xml += '\n\t<Sensor>\n\t\t<sensor_id>' + id + '</sensor_id>'
                                    xml += '\n\t\t<patient_id>' + patient_id + '</patient_id>'
                                    xml += '\n\t\t<sensor_type>' + sensor_type + '</sensor_type>'
                                    xml += '\n\t\t<location_name>' + sensor_location + '</location_name>'
                                    xml += '\n\t\t<location_id>' + sensor_type + '</location_id>'
                                    xml += '\n\t\t<sensor_location_id>' + sensor_location_id + '</sensor_location_id>'
                                    xml += '\n\t\t<is_connected>TRUE</is_connected>'
                                    xml += '\n\t</Sensor>'

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
                                    
                                    xml += '\n\t<Activity>\n\t\t<activity_id>' + id + '</activity_id>'
                                    xml += '\n\t\t<activity_type>' + activity_type + '</activity_type>'
                                    xml += '\n\t\t<start_time>' + str(start_time) + '</start_time>'
                                    xml += '\n\t\t<end_time>' + str(end_time) + '</end_time>'
                                    xml += '\n\t\t<is_uploaded>TRUE</is_uploaded>'
                                    xml += '\n\t\t<patient_id>' + patient_id + '</patient_id>'
                                    xml += '\n\t</Activity>'

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

                                    
                                    n = max(1, min(sensors - i, sensors))
                                    sensor = patients_sensors[n - 1]

                                    for _ in range(n):
                                        start_time, end_time = activity.start_time, activity.end_time
                                        id = str(uuid4())
                                        pressure_value = fake.random_int(min=0, max=100)
                                        pressure_value += fake.random_int(min=-45, max=45)


                                        xml += '\n\t<ActivityReading>\n\t\t<activity_id>' + activity.activity_id + '</activity_id>'
                                        xml += '\n\t\t<reading_series_id>' + id + '</reading_series_id>'
                                        xml += '\n\t\t<sensor_id>' + sensor.sensor_id + '</sensor_id>'
                                        xml += '\n\t</ActivityReading>'  

                                        for timestamp in range(start_time, end_time + 1):
                                            pressure_reading_id = str(uuid4())

                                            xml += '\n\t<PressureReading>\n\t\t<pressure_reading_id>' + pressure_reading_id + '</pressure_reading_id>'
                                            xml += '\n\t\t<pressure_value>' + str(pressure_value) + '</pressure_value>'
                                            xml += '\n\t\t<time>' + str(timestamp) + '</time>'
                                            xml += '\n\t\t<is_uploaded>TRUE</is_uploaded>'
                                            xml += '\n\t\t<reading_series_id>' + id + '</reading_series_id>'
                                            xml += '\n\t</PressureReading>'        
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
                    progress_bar = ui.linear_progress(value=0, color="#FFB030", show_value=False).classes('w-full rounded') 
                



            
