from nicegui import ui
import Homepage
import DatabaseConfig

def header():
    with ui.header().style('background-color: #FFFFFF'):
        with ui.row().classes('w-full justify-center items-center'):
            ui.image('SocketFitDashboard.png').classes('h-[40px] w-[140px]')

@ui.page('/login')
def login():
    ui.page_title("SocketFit Dashboard")
    header()
    with ui.row().classes('w-full h-full justify-center items-center'):
        with ui.card().classes('w-[300px] border rounded-md border-[#2C25B2]'):
            ui.input(placeholder='Email').classes('w-full border rounded-md border-[#3545FF]')
            ui.input(placeholder='Password').classes('w-full border rounded-md border-[#3545FF]')
            ui.button('Login', on_click=Homepage.mainNavigate, color='#FFB030').classes('w-full text-white')
            ui.button('Login as IT Admin', color='#3545FF', on_click=DatabaseConfig.navigateConfig).classes('w-full text-white')

ui.run(favicon="SocketFit logo.png")
ui.navigate.to('/login')