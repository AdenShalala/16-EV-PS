from nicegui import ui, app
import requests
from pages.utilities import header


def create() -> None:
    @ui.page('/test')
    def login():
        # comparing entered value
        def checkLogin():
            #app.storage.user['clinid'] = email.value
            #print(requests.post("http://localhost:8000/login", {'username': email.value, 'password': password.value}))

            print()

            #Homepage.mainNavigate()
        ui.page_title("SocketFit Dashboard")
        header()
        
        with ui.row().classes('w-full h-full justify-center items-center'):
            # login box
            with ui.card().classes('w-[300px] border rounded-md border-[#2C25B2]'):
                email = ui.input(placeholder='Email').classes('w-full border rounded-md border-[#3545FF] left-2')
                password = ui.input(placeholder='Password').classes('w-full border rounded-md border-[#3545FF]')
                ui.button('Login', on_click=checkLogin, color='#FFB030').classes('w-full text-white')
                #ui.button('Login as IT Admin', color='#3545FF', on_click=DatabaseConfig.navigateConfig).classes('w-full text-white')