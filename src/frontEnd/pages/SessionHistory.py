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
    app.storage.user['activityList'] = []
    for activity in patient.activities:
        app.storage.user['activityList'].append(activity)
    activityNameList = ['All']
    app.storage.user['actTypeList'] = ['All']
    for app.storage.user['activity'] in app.storage.user.get('activityList'):
        # print(activity.type)
        app.storage.user['actTypeList'].append(activity.type)
        # print(app.storage.user.get('actTypeList'))
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
                ui.select(options=app.storage.user.get('actTypeList'), value=app.storage.user.get('actTypeList', [])[0]).classes('col-span-2 w-full border rounded-md border-[#3545FF]')
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
                    for app.storage.user['activity'] in app.storage.user.get('activityList'):
                        app.storage.user['dt_str1'] = app.storage.user.get('activity').start_time
                        app.storage.user['dt_str2'] = app.storage.user.get('activity').end_time

                        dt_format = "%d-%b-%Y %H:%M:%S"

                        dt1 = datetime.strptime(app.storage.user.get('dt_str1'), dt_format)
                        dt2 = datetime.strptime(app.storage.user.get('dt_str2'), dt_format)

                        # app.storage.user['duration'] = dt2 - dt1
                        total_seconds = int((dt2 - dt1).total_seconds())
                        app.storage.user['total_seconds'] = total_seconds

                        # app.storage.user['total_seconds'] = int(app.storage.user.get('duration').total_seconds())

                        app.storage.user['hours'] = app.storage.user.get('total_seconds') // 3600
                        app.storage.user['minutes'] = (app.storage.user.get('total_seconds') % 3600) // 60
                        app.storage.user['seconds'] = app.storage.user['total_seconds'] % 60

                        app.storage.user['minSensor'] = None
                        app.storage.user['maxSensor'] = None
                        for app.storage.user['sensor'] in app.storage.user.get('activity').sensors:
                            for app.storage.user['signal'] in app.storage.user.get('sensor').signal:
                                if app.storage.user.get('minSensor') == None or float(app.storage.user.get('signal')) < float(app.storage.user.get('minSensor')):
                                    app.storage.user['minSensor'] = round(float(app.storage.user.get('signal')), 1)
                                if app.storage.user.get('maxSensor') == None or float(app.storage.user.get('signal')) > float(app.storage.user.get('maxSensor')):
                                    app.storage.user['maxSensor'] = round(float(app.storage.user.get('signal')), 1)

                        print(app.storage.user.get('minSensor'))
                        print(app.storage.user.get('maxSensor'))

                        print(f"Duration: {app.storage.user.get('hours')} hours, {app.storage.user.get('minutes')} minutes, {app.storage.user.get('seconds')} seconds")
                        with ui.grid(columns=23).classes('border-[2px] border-[#2C25B2] rounded items-center'):
                            ui.label('').classes('col-span-1')
                            ui.label(f'This is row ').classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(app.storage.user.get('activity').start_time).classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(app.storage.user.get('activity').type).classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(f'{app.storage.user.get('hours')}h{app.storage.user.get('minutes')}m{app.storage.user.get('seconds')}s').classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(f"{app.storage.user.get('minSensor')} - {app.storage.user.get('maxSensor')}").classes('col-span-2')
                            ui.button('View Activity').props('flat').classes(
                                      'col-span-4 text-white text-sm px-3 py-1 rounded-3xl bg-[#FFB030] h-1/2'
                                     ).on_click(partial(activitypass, app.storage.user.get('activity')))
                ui.space()


def navigateSession():
    ui.navigate.to('sessionHistory')

def navigatePatientSession(patient):
    app.storage.user['patient'] = patient
    ui.navigate.to('/sessionHistory')