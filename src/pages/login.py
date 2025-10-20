from nicegui import ui, app
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
import api

def create() -> None:
    @ui.page('/login')
    def test():
            # Dialog for login error, hidden by default
        with ui.dialog() as error_dialog, ui.card():
            ui.label('Invalid email or password. Please try again.').classes('text-red-500 text-center')
            ui.button('OK', on_click=error_dialog.close, color='#FFB030').classes('w-full text-white mt-2')
            
        def checkLogin():
            try:
                # Attempt to log in
                x = api.token(OAuth2PasswordRequestForm(password=password.value, username=email.value))
                app.storage.user['token'] = x['access_token']

                if x["type"] == "Clinician":
                    ui.navigate.to('/')
                else:
                    ui.navigate.to('/admin')
            
            except Exception as e:
                # If login fails, it will show dialog with error message
                ui.notify('Invalid email or password. Please try again.', color='red')
                # error_dialog.open()

        ui.page_title("SocketFit Dashboard")
        with ui.header().style('background-color: #FFFFFF'):
            with ui.row().classes('w-full justify-center items-center'):
                ui.image('src/assets/dashboard.png').classes('h-[40px] w-[140px]')
        
        with ui.row().classes('w-full h-full justify-center items-center'):
            with ui.card().classes('w-[300px] border rounded-md border-[#2C25B2]'):
                email = ui.input(placeholder='Email').classes('w-full border rounded-md border-[#3545FF] left-2').on('keydown.enter', checkLogin)
                password = ui.input(password=True, placeholder='Password').classes('w-full border rounded-md border-[#3545FF]').on('keydown.enter', checkLogin)
                ui.button('Login', on_click=checkLogin, color='#FFB030').classes('w-full text-white')
                ui.label('Example username: amy.adams@clinician.com').classes('text-center text-gray-500 text-sm mt-2')