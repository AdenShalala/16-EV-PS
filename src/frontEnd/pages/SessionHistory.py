from nicegui import ui, app
import utilities
import ActivityPage
from datetime import datetime
from functools import partial
from collections import OrderedDict

# getting standard header
def header():
    utilities.header()

# getting activity and navigating
def activitypass(act):
    app.storage.user['activity'] = act
    ActivityPage.navigateActivity()

def normalize_to_str(value: str | int | float | datetime) -> str:
    """Return time as 'dd-Mon-YYYY HH:MM:SS' string, no tzinfo."""
    if value is None:
        return None

    # if it's already a datetime
    if isinstance(value, datetime):
        return value.strftime("%d-%b-%Y %H:%M:%S")

    # if it's a unix timestamp
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        dt = datetime.fromtimestamp(int(value))
        return dt.strftime("%d-%b-%Y %H:%M:%S")

    # if it's a string datetime
    value = str(value).strip()
    formats = [
        "%Y-%m-%d %H:%M:%S%z",   # 2023-08-28 12:33:20+00:00
        "%Y-%m-%d %H:%M:%S",     # 2023-08-28 12:33:20
        "%Y-%m-%dT%H:%M:%S",     # 2023-08-28T12:33:20
        "%d-%b-%Y %H:%M:%S",     # 28-Aug-2023 12:33:20
        "%d %b %Y",              # 28 Aug 2023
        "%Y-%m-%d"               # 2023-08-28
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%d-%b-%Y %H:%M:%S")
        except ValueError:
            continue

    raise ValueError(f"Unsupported datetime format: {value!r}")

@ui.page('/sessionHistory')
def sessionHistory():
    app.storage.user['current_page'] = '/sessionHistory'
    ui.page_title("SocketFit Dashboard")
    header()
    app.storage.user['actTypeList'] = ['All']
    
    for app.storage.user['activity'] in app.storage.user.get('patient').activities:
        # adding unique activity types to list
        if app.storage.user.get('activity').type not in app.storage.user.get('actTypeList'):
            app.storage.user['actTypeList'].append(app.storage.user['activity'].type)
    with ui.row().classes('w-full'):
        ui.label("User History").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-full'):
        # left section with tree
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            utilities.session_tree()
        # main section
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            # filter titles
            ui.label("Filters:")
            with ui.grid(columns=11).classes('w-full'):
                ui.label("Activity").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label("Duration").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label("Pressure Range").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label('Pressure Tolerance').classes('col-span-2')
            # filter boxes
            with ui.grid(columns=11).classes('w-full'):
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
                # titles for session activities
                with ui.card().classes('w-9/10 border rounded-md border-[#3545FF]'):
                    with ui.grid(columns=24):
                        ui.label('').classes('col-span-1')
                        ui.label('Date').classes('col-span-3')
                        ui.label('').classes('col-span-3')
                        ui.label('Activity').classes('col-span-2')
                        ui.label('').classes('col-span-3')
                        ui.label('Duration').classes('col-span-2')
                        ui.label('').classes('col-span-3')
                        ui.label('Pressure').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('').classes('col-span-3')

                    # calculating duration of activities
                    for app.storage.user['current_activity'] in app.storage.user.get('patient').activities:
                        
                        app.storage.user['dt_str1'] = normalize_to_str(app.storage.user['current_activity'].start_time)
                        app.storage.user['dt_str2'] = normalize_to_str(app.storage.user['current_activity'].end_time)

                        dt_format = "%d-%b-%Y %H:%M:%S"

                        dt1 = datetime.strptime(app.storage.user['dt_str1'], dt_format)
                        dt2 = datetime.strptime(app.storage.user['dt_str2'], dt_format)

                        total_seconds = int((dt2 - dt1).total_seconds())
                        app.storage.user['total_seconds'] = total_seconds

                        app.storage.user['hours'] = app.storage.user['total_seconds'] // 3600
                        app.storage.user['minutes'] = (app.storage.user['total_seconds'] % 3600) // 60
                        app.storage.user['seconds'] = app.storage.user['total_seconds'] % 60

                        app.storage.user['minSensor'] = None
                        app.storage.user['maxSensor'] = None
                        
                        # finding min and max sensor signal values
                        current_activity = app.storage.user['current_activity']  # Store reference for cleaner access

                        for sensor in current_activity.sensors:
                            for reading in sensor.readings:
                                if reading.activity_id == current_activity.activity_id:
                                    value = float(reading.pressure_value)

                                    if app.storage.user['minSensor'] is None or value < app.storage.user['minSensor']:
                                        app.storage.user['minSensor'] = round(value, 1)

                                    if app.storage.user['maxSensor'] is None or value > app.storage.user['maxSensor']:
                                        app.storage.user['maxSensor'] = round(value, 1)

                        # creating row for each activity
                        with ui.grid(columns=24).classes('border-[2px] border-[#2C25B2] h-16 rounded items-center'):
                            ui.label('').classes('col-span-1')
                            ui.label(normalize_to_str(app.storage.user.get('activity').start_time)).classes('col-span-3')
                            ui.label('').classes('col-span-3')
                            ui.label(app.storage.user.get('current_activity').type).classes('col-span-2')
                            ui.label('').classes('col-span-3')
                            ui.label(f'{app.storage.user.get('hours')}h{app.storage.user.get('minutes')}m{app.storage.user.get('seconds')}s').classes('col-span-2')
                            ui.label('').classes('col-span-3')
                            ui.label(f"{app.storage.user.get('minSensor')} - {app.storage.user.get('maxSensor')}").classes('col-span-2')
                            ui.button('View Activity').props('flat').classes(
                                      'col-span-5 text-white text-sm px-3 py-1 rounded-3xl bg-[#FFB030] h-1/2'
                                     ).on_click(partial(activitypass, app.storage.user.get('current_activity')))
                ui.space()

def navigateSession():
    ui.navigate.to('sessionHistory')

def navigatePatientSession(patient):
    app.storage.user['patient'] = patient
    ui.navigate.to('/sessionHistory')