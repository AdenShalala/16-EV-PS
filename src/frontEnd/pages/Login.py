from nicegui import ui, app
import Homepage
import DatabaseConfig
import AdminHomepage

# login header
def header():
    with ui.header().style('background-color: #FFFFFF'):
        with ui.row().classes('w-full justify-center items-center'):
            ui.image('src\\frontEnd\\assets\\SocketFitDashboard.png').classes('h-[40px] w-[140px]')

@ui.page('/login')
def login():
    # comparing entered value
    def checkLogin():
        app.storage.user['clinid'] = email.value
        Homepage.mainNavigate()

    ui.page_title("SocketFit Dashboard")
    header()
    with ui.row().classes('w-full h-full justify-center items-center'):
        # login box
        with ui.card().classes('w-[300px] border rounded-md border-[#2C25B2]'):
            email = ui.input(placeholder='Email').classes('w-full border rounded-md border-[#3545FF]')
            ui.input(placeholder='Password').classes('w-full border rounded-md border-[#3545FF]')
            ui.button('Login', on_click=checkLogin, color='#FFB030').classes('w-full text-white')
            ui.button('Login as IT Admin', color='#3545FF', on_click=AdminHomepage.navigateAdminHome).classes('w-full text-white')

ui.run(storage_secret='this is the very secret key', favicon="src\\frontEnd\\assets\\SocketFit Logo.png")
ui.navigate.to('/login')