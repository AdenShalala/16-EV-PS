from nicegui import ui
import elements

def header():
    elements.header()

def on_tree_select(e):
    label_to_path = {
        'User Information': '/userInformation',
        'Session History': '/sessionHistory',
    }

    selected_label = e.value
    if selected_label in label_to_path:
        ui.navigate.to(label_to_path[selected_label])
    else:
        ui.notify(f'Selected: {selected_label}')

@ui.page('/sessionHistory')
def sessionHistory():
    ui.page_title("SocketFit Dashboard")
    header()
    activityList = ['All']
    with ui.row().classes('w-full'):
        ui.label("User History").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[800px]'):
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            ui.link('Patients', '/main').classes('text-black text-xl no-underline cursor-pointer')
            current_page = 'User Information'
            with ui.expansion(text="User Records"):
                with ui.expansion(text='User Information'):
                    ui.label("here")
                ui.label('Session History').classes('font-bold')

            tree_data = [
                {
                    'id': 'User Records',
                    'children': [
                        {
                            'id': 'User Information',
                            'label': f'User Information'
                        },
                        {
                            'id': 'Session History',
                            'label': f'<b>Session History</b>'
                        }
                    ]
                }
            ]

            tree = ui.tree(
                tree_data, 
                label_key='label', 
                # default_value=current_page,
                on_select=on_tree_select
            )
            ui.label('User Records').classes('font-bold text-xl')
            ui.link('User Information', '/userInformation').classes('text-black no-underline cursor-pointer')
            ui.label("Session History").classes('font-bold')
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
                ui.select(options=activityList, value=activityList[0]).classes('col-span-2 w-full border rounded-md border-[#3545FF]')
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
                    for i in range(1, 6):
                        with ui.grid(columns=23).classes('border-[2px] border-[#2C25B2] rounded'):
                            ui.label('').classes('col-span-1')
                            ui.label(f'This is row {i}').classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(f'Where patient {i} is').classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(f'Data chunk {i}').classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(f'Duration {i}').classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.label(f'Pressure {i}').classes('col-span-2')
                            ui.button('View Activity').props('flat').classes(
                                      'col-span-4 text-white text-sm px-3 py-1 rounded-md bg-[#FFB030]'
                                     )
                ui.space()


def navigateSession():
    ui.navigate.to('sessionHistory')