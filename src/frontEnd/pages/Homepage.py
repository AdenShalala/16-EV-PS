from nicegui import ui, app
import elements
import UserInformation
import Login
import ActivityPage
import os
import sys
from utilities import session_tree

sql_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src', 'backEnd', 'databases', 'SQL'))
if sql_path not in sys.path:
    sys.path.insert(0, sql_path)
try:
    from SQL_read import read_patients_by_clinician_id
except ImportError as e:
    raise ImportError(f"Could not import 'SQL_read'. Make sure 'SQL_read.py' exists in {sql_path}. Original error: {e}")

def header():
    elements.header()

@ui.page('/main')
def main():
    app.storage.user['current_page'] = '/main'
    patients = read_patients_by_clinician_id(app.storage.user.get('clinid'))
    app.storage.user['patients'] = patients
    patients = None
    # print(app.storage.user.get('patients'))
    
    # print(app.storage.user.get('clinid'))
    ui.page_title("SocketFit Dashboard")
    genderList = ['All', 'Male', 'Female', 'Prefer not to say']
    amputationTypeList = ['All']
    header()
    with ui.row().classes('w-full'):
        ui.label("Welcome").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[500px]'):
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]'):
            ## Tree with users needed
            # session_tree()
            print('working')
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            with ui.row().classes('w-full'):
                ui.label("Select User to View Users Information").classes('text-lg font-bold')
                ui.space()
                ui.input(label="Search Name", placeholder='Name').classes('border rounded-md border-[#3545FF]')
            ui.label("Filters").classes('text-md font-semibold')

            with ui.grid(columns=10).classes('w-full gap-4'):
                ui.label("Gender:").classes('col-span-2')
                ui.label("Age:").classes('col-span-2')
                ui.label("Height (cm):").classes('col-span-2')
                ui.label("Weight (kg):").classes('col-span-2')
                ui.label("Amputation Type:").classes('col-span-2')

            with ui.grid(columns=10).classes('w-full gap-4'):
                ui.select(value=genderList[0], options=genderList).classes('col-span-2 border rounded-md border-[#3545FF]')

                with ui.row().classes('col-span-2 gap-1'):
                    ui.number(label="Min", placeholder="Min").classes('w-2/5 border rounded-md border-[#3545FF]')
                    ui.number(label="Max", placeholder="Max").classes('w-2/5 border rounded-md border-[#3545FF]')

                with ui.row().classes('col-span-2 gap-1'):
                    ui.number(label="Min", placeholder="Min").classes('w-2/5 border rounded-md border-[#3545FF]')
                    ui.number(label="Max", placeholder="Max").classes('w-2/5 border rounded-md border-[#3545FF]')

                with ui.row().classes('col-span-2 gap-1'):
                    ui.number(label="Min", placeholder="Min").classes('w-2/5 border rounded-md border-[#3545FF]')
                    ui.number(label="Max", placeholder="Max").classes('w-2/5 border rounded-md border-[#3545FF]')

                ui.select(value=amputationTypeList[0], options=amputationTypeList).classes('col-span-2 border rounded-md border-[#3545FF]')
            def test(patient):
                print(patient.month_year_birth)

            with ui.grid(columns=4).classes('w-full gap-6'):
                for patient in app.storage.user.get('patients'):
                    app.storage.user['gender'] = patient.gender
                    app.storage.user['dob'] = patient.month_year_birth
                    with ui.card().classes('h-[150px] w-[160px] border border-[#2C25B2]').on('click', lambda: UserInformation.navigatePatient(patient)):
                        ui.label('User').classes('text-xl')
                        ui.label(app.storage.user.get('dob'))
                        ui.label(app.storage.user.get('gender'))
    ui.button('test', on_click=UserInformation.navigate)
    ui.button('activity', on_click=ActivityPage.navigateActivity)

def mainNavigate():
    ui.navigate.to('/main')

# ui.run(storage_secret='this is the very secret key', favicon="SocketFit Logo.png") 
ui.navigate.to('/main')