from nicegui import ui, app
import utilities
import UserInformation
import Login
import ActivityPage
import os
import sys

sql_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src', 'backEnd', 'databases', 'SQL'))
if sql_path not in sys.path:
    sys.path.insert(0, sql_path)
try:
    from SQL_read import read_patients_by_clinician_id
except ImportError as e:
    raise ImportError(f"Could not import 'SQL_read'. Make sure 'SQL_read.py' exists in {sql_path}. Original error: {e}")

def header():
    utilities.header()

@ui.page('/main')
def main():
    app.storage.user['current_page'] = '/main'
    app.storage.user['patients'] = read_patients_by_clinician_id(app.storage.user.get('clinid'))

    ui.page_title("SocketFit Dashboard")
    genderList = ['All', 'Male', 'Female', 'Prefer not to say']
    amputationTypeList = ['All']
    app.storage.user['activityList'] = []
    # looping through patients
    for app.storage.user['patient'] in app.storage.user.get('patients'):
        for app.storage.user['activity'] in app.storage.user.get('patient').activities:
            app.storage.user['activityList'].append(app.storage.user['activity'])
    header()
    with ui.row().classes('w-full'):
        ui.label("Welcome").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[500px]'):
        # side tree section
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]'):
            # Tree with users needed
           utilities.patients_tree()
        # main section
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            with ui.row().classes('w-full'):
                ui.label("Select User to View Users Information").classes('text-lg font-bold')
                ui.space()
                ui.input(label="Search Name", placeholder='Name').classes('border rounded-md border-[#3545FF]')
            ui.label("Filters").classes('text-md font-semibold')

            # filter titles
            with ui.grid(columns=10).classes('w-full gap-4'):
                ui.label("Gender:").classes('col-span-2')
                ui.label("Age:").classes('col-span-2')
                ui.label("Height (cm):").classes('col-span-2')
                ui.label("Weight (kg):").classes('col-span-2')
                ui.label("Amputation Type:").classes('col-span-2')

            # filter boxes
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

            with ui.grid(columns=4).classes('w-full gap-6'):
                # storing patient information
                for app.storage.user['patient'] in app.storage.user.get('patients'):
                    app.storage.user['gender'] = app.storage.user.get('patient').gender
                    app.storage.user['dob'] = app.storage.user.get('patient').month_year_birth
                    # displaying each user in separate cards
                    with ui.card().classes('h-[150px] w-[160px] border border-[#2C25B2] cursor-pointer').on('click', lambda: UserInformation.navigatePatient(app.storage.user.get('patient'))):
                        ui.label('User').classes('text-xl')
                        ui.label(app.storage.user.get('dob'))
                        ui.label(app.storage.user.get('gender'))

def mainNavigate():
    ui.navigate.to('/main')

ui.navigate.to('/main')