from nicegui import ui, app
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
import api


def create() -> None:
    @ui.page('/login')
    def test():
        def checkLogin():
            x = api.token(OAuth2PasswordRequestForm(password=password.value, username=email.value))
            app.storage.user['token'] = x['access_token']

            if x["type"] == "Clinician":
                ui.navigate.to('/')
            else:
                ui.navigate.to('/admin')

        ui.page_title("SocketFit Dashboard")
        with ui.header().style('background-color: #FFFFFF'):
            with ui.row().classes('w-full justify-center items-center'):
                ui.image('src/assets/dashboard.png').classes('h-[40px] w-[140px]')
        
        with ui.row().classes('w-full h-full justify-center items-center'):
            with ui.card().classes('w-[300px] border rounded-md border-[#2C25B2]'):
                email = ui.input(placeholder='Email').classes('w-full border rounded-md border-[#3545FF] left-2')
                password = ui.input(password=True, placeholder='Password').classes('w-full border rounded-md border-[#3545FF]')
                ui.button('Login', on_click=checkLogin, color='#FFB030').classes('w-full text-white')