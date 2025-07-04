from nicegui import ui
import elements
import UserInformation
import Login
import Activity

def header():
    elements.header()

@ui.page('/main')
def main():
    genderList = ['All', 'Male', 'Female', 'Prefer not to say']
    amputationTypeList = ['All']
    header()
    with ui.row().classes('w-full'):
        ui.label("Welcome").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[500px]'):
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            ui.label("Patients")
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

            with ui.grid(columns=4).classes('w-full gap-6'):
                ui.card().classes('h-[150px] w-[160px] border border-[#2C25B2]')
    ui.button('test', on_click=UserInformation.navigate)
    ui.button('activity', on_click=Activity.navigateActivity)

def mainNavigate():
    ui.navigate.to('/main')

ui.run()
ui.navigate.to('/main')