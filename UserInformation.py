from nicegui import ui
import elements
import SessionHistory

def header():
    elements.header()

@ui.page('/userInformation')
def main():
    ui.page_title("SocketFit Dashboard")
    header()
    with ui.row().classes('w-full'):
        ui.label("User").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[800px]'):
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            ui.label("User Records")
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            with ui.row():
                with ui.row().classes('w-2/5 items-start'):
                    ui.input(placeholder='Users First Name', label='First Name').classes('w-full border rounded-md border-[#3545FF]')
                    ui.input(placeholder='Users Last Name', label='Last Name').classes('w-full border rounded-md border-[#3545FF]')
                    ui.input(placeholder='Users Date of Birth', label='Date of Birth').classes('w-full border rounded-md border-[#3545FF]')
                    ui.input(placeholder='Users Weight', label='Weight (kg)').classes('w-full border rounded-md border-[#3545FF]')
                    ui.input(placeholder='Users Gender', label='Gender').classes('w-full border rounded-md border-[#3545FF]')
                    ui.input(placeholder='Users Height', label='Height (cm)').classes('w-full border rounded-md border-[#3545FF]')
                    ui.input(placeholder='Users Amputation Type', label='Amputation Type').classes('w-full border rounded-md border-[#3545FF]')
                ui.space()
                with ui.column().classes('w-2/5'):
                    ui.label("Additional Notes").classes('text-xl self-start')
                    ui.textarea(placeholder='Enter Notes Here').classes('h-full w-full border rounded-md border-[#3545FF]')
    ui.button("Next", on_click=SessionHistory.navigateSession)
def navigate():
    ui.navigate.to('/userInformation')