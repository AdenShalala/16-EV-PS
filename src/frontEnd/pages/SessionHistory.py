from nicegui import ui, app
import elements
import ActivityPage
from datetime import datetime
from functools import partial
from utilities import bold, on_tree_select

def header():
    elements.header()

def activitypass(act):
    app.storage.user['activity'] = act
    ActivityPage.navigateActivity()



@ui.page('/sessionHistory')
def sessionHistory():
    app.storage.user['current_page'] = '/sessionHistory'
    patient = app.storage.user.get('patient')
    ui.page_title("SocketFit Dashboard")
    header()
    activityList = []
    for activity in patient.activities:
        activityList.append(activity)
    activityNameList = ['All']
    with ui.row().classes('w-full'):
        ui.label("User History").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[800px]'):
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:

            current_page = app.storage.user.get('current_page', '')

            tree_data = [
                {
                    'id': 'User Records',
                    'label': 'User Records',
                    'children': [
                        {
                            'id': 'User Information',
                            'label': bold('User Information') if current_page == '/userInformation' else 'User Information'
                        },
                        {
                            'id': 'Session History',
                            'label': bold('Session History') if current_page == '/sessionHistory' else 'Session History'
                        }
                    ]
                }
            ]

            tree = ui.tree(
                tree_data, 
                label_key='label', 
                # default_value=current_page,
                on_select=on_tree_select
            ).expand(['User Records'])
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            ui.label("Filters:")
            with ui.grid(columns=11).classes('w-full'):
                # ui.label('').classes('col-span-1')
                ui.label("Activity").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label("Duration").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label("Pressure Range").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label('Pressure Tolerance').classes('col-span-2')
                # ui.label('').classes('col-span-1')
            with ui.grid(columns=11).classes('w-full'):
                # ui.label('').classes('col-span-1')
                ui.select(options=activityNameList, value=activityNameList[0]).classes('col-span-2 w-full border rounded-md border-[#3545FF]')
                ui.label('').classes('col-span-1')
                ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.label('').classes('col-span-1')
                ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.label('').classes('col-span-1')
                ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
            ui.label("Session List").classes('text-2xl')
            with ui.row().classes('w-full'):
                ui.space()
                with ui.card().classes('w-9/10 border rounded-md border-[#3545FF]'):
                    with ui.grid(columns=23):
                        ui.label('').classes('col-span-1')
                        ui.label('Session ID').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('Date').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('Activity').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('Duration').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('Pressure').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                    #This is an example of how these details would be listed.
                    #It would be 'for activity in activities:'
                    # for i in range(1, 6):
                    for activity in activityList:
                        dt_str1 = activity.start_time
                        dt_str2 = activity.end_time

                        dt_format = "%d-%b-%Y %H:%M:%S"

                        dt1 = datetime.strptime(dt_str1, dt_format)
                        dt2 = datetime.strptime(dt_str2, dt_format)

                        duration = dt2 - dt1

                        total_seconds = int(duration.total_seconds())

                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        seconds = total_seconds % 60

                        print(f"Duration: {hours} hours, {minutes} minutes, {seconds} seconds")
                        with ui.grid(columns=23).classes('border-[2px] border-[#2C25B2] rounded'):
                            ui.label('').classes('col-span-1')
                            ui.label(f'This is row ').classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(activity.start_time).classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(activity.type).classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(f'{hours}h{minutes}m{seconds}s').classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(f'Pressure ').classes('col-span-2')
                            ui.button('View Activity').props('flat').classes(
                                      'col-span-4 text-white text-sm px-3 py-1 rounded-md bg-[#FFB030]'
                                     ).on_click(partial(activitypass, activity))
                ui.space()


def navigateSession():
    ui.navigate.to('sessionHistory')

def navigatePatientSession(patient):
    app.storage.user['patient'] = patient
    ui.navigate.to('/sessionHistory')