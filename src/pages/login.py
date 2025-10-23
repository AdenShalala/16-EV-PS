from nicegui import ui, app
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
import api

def create() -> None:
    # login page
    @ui.page('/login')
    def login():
        # checking dark mode status
        async def get_dark_mode():
            enabled = await ui.run_javascript('Quasar.Dark.isActive')
            app.storage.user["dark_mode"] = enabled

        dark = ui.dark_mode(on_change=get_dark_mode)
        # set dark mode based on users default preference
        dark.auto()
        
        # check login credentials
        def checkLogin():
            try:
                # attempt to log in
                x = api.token(OAuth2PasswordRequestForm(password=password.value, username=email.value))
                app.storage.user['token'] = x['access_token']

                if x["type"] == "Clinician":
                    ui.navigate.to('/')
                else:
                    ui.navigate.to('/admin')
            
            except Exception as e:
                # if login fails, it will show dialog with error message
                ui.notify('Invalid email or password. Please try again.', color='red')

        # setting page title
        ui.page_title("SocketFit Dashboard")
        # creating header
        with ui.header(elevated=False).classes('bg-[#ffffff] dark:bg-[#121212]'):
            with ui.row().classes('w-full justify-center items-center'):
                ui.image('/assets/dashboard.png').classes('h-[40px] w-[140px]')
        
        # creating login card
        with ui.row().classes('w-full h-full justify-center items-center'):
            with ui.card().classes('w-[300px] bg-[#F5F5F5] dark:bg-[#1d1d1d] border rounded-md border-[#2C25B2] no-shadow'):
                email = ui.input(placeholder='Email').classes('w-full border rounded-md border-[#3545FF] p-1').on('keydown.enter', checkLogin)
                password = ui.input(password=True, placeholder='Password', password_toggle_button=True).classes('w-full border rounded-md border-[#3545FF] p-1').on('keydown.enter', checkLogin)
                ui.button('Login', on_click=checkLogin, color='#FFB030').classes('w-full text-white')