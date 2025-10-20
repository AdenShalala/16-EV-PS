from nicegui import ui, app
import api
import pages.utilities as utilities
from schema import Clinician, Admin

def logout():
    api.logout(token=app.storage.user.get("token"))
    app.storage.user.clear()
    ui.navigate.to('/login')

def create() -> None:
    @ui.page('/account')
    def account():
        app.storage.user['current_page'] = '/account'
        account = api.get_me(token=app.storage.user.get("token", None))
        utilities.header()
        
        ui.page_title('SocketFit Dashboard')
        
        id = ""

        if type(account) == Clinician:
            left_drawer = utilities.sidebar()
            utilities.arrow(left_drawer=left_drawer)
            id = account.clinician_id
        elif type(account) == Admin: 
            left_drawer = utilities.admin_sidebar()
            utilities.arrow(left_drawer=left_drawer)

            id = account.admin_id       


        with ui.row().classes(' w-full flex justify-center'):
            with ui.card().classes('w-2/5 justify-center items-center bg-[#F5F5F5] dark:bg-[#1d1d1d] border border-[#2C25B2] no-shadow'):
                if not account:
                    ui.label('Account not loaded yet.').classes('p-4 text-gray-600')
                    return
                
                with ui.row().classes('w-full'):
                    with ui.grid(rows=2, columns=1).classes(replace=''):
                        ui.label(f"{account.first_name} {account.last_name}").classes('font-bold text-xl dark:text-white')
                        ui.label(id).classes('text-xs text-grey')


                    with ui.row().classes('w-full items-start'):
                        first_name = ui.input(label='First Name', value=account.first_name).classes('w-full border rounded-md border-[#3545FF] p-1')
                        last_name = ui.input(label='Last Name', value=account.last_name).classes('w-full border rounded-md border-[#3545FF] p-1')
                        email = ui.input(label='Email', value=account.email).classes('w-full border rounded-md border-[#3545FF] p-1')


                        def save():
                            if not utilities.validate_email(email.value):
                                ui.notify('Invalid email', color='red')
                                return
                            
                            if len(first_name.value) < 1 or len(last_name.value) < 1:
                                ui.notify('Invalid name', color='red')
                                return                                
                            
                            if type(account) == Clinician:
                                if not api.verify_email(email.value):
                                    ui.notify('Email is taken', color='red')
                            elif type(account) == Admin: 
                                if not api.verify_admin_email(email.value):
                                    ui.notify('Email is taken', color='red')

                            account.first_name = first_name.value
                            account.last_name = last_name.value
                            account.email = email.value
                            api.put_me(account, token=app.storage.user.get("token"))
                            ui.run_javascript('location.reload();')



                        with ui.row().classes('w-full items-center justify-between'):
                            ui.button('Save', on_click=save, color='#FFB030').classes('text-white rounded-md px-6 py-2')
                            ui.button('Logout', on_click=logout, color='#FFB030').classes('text-white rounded-md px-6 py-2')




                # # user information boxes

