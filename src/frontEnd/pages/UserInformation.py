from nicegui import ui, app
import utilities
import SessionHistory


def header():
    utilities.header()


    
@ui.page('/userInformation')
def main():
    app.storage.user['current_page'] = '/userInformation'
    patient = app.storage.user.get('patient')
    ui.page_title("SocketFit Dashboard")
    header()
    with ui.row().classes('w-full'):
        ui.label("User").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[800px]'):
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            utilities.session_tree()
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            with ui.row():
                with ui.row().classes('w-2/5 items-start'):
                    with ui.input(placeholder='Users First Name', label='First Name').classes('w-full h-full border rounded-md border-[#3545FF]'):
                        ui.icon('o_edit').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(placeholder='Users Last Name', label='Last Name').classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('o_edit').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(placeholder='Users Date of Birth', label='Date of Birth', value = patient.month_year_birth).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('o_calendar_month').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(placeholder='Users Weight', label='Weight (kg)', value=patient.weight).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('o_edit').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(placeholder='Users Gender', label='Gender', value=patient.gender).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('o_edit').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(placeholder='Users Height', label='Height (cm)', value=patient.height).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('o_edit').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(placeholder='Users Amputation Type', label='Amputation Type', value=patient.amputation_type).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('o_edit').classes('text-black text-3xl h-full flex items-center mr-2')
                ui.space()
                with ui.column().classes('w-2/5'):
                    ui.label("Additional Notes").classes('text-xl self-start')
                    ui.textarea(placeholder='Enter Notes Here').classes('h-full w-full border rounded-md border-[#3545FF]')
def navigate():
    ui.navigate.to('/userInformation')

def navigatePatient(patient):
    app.storage.user['patient'] = patient
    ui.navigate.to('/userInformation')