
from nicegui import ui, app
import pages.utilities as utilities
import api
from functools import partial


def navigate_clinician(clinician):
    app.storage.user['selected_clinician'] = clinician.clinician_id
    ui.navigate.to("/clinician")



def create() -> None:
    @ui.page('/admin')
    def admin():
        app.storage.user['current_page'] = '/admin'
        ui.page_title('SocketFit Admin')
        utilities.header()
        left_drawer = utilities.admin_sidebar()
        

        clinicians = api.get_clinicians(app.storage.user.get("token"))


        with ui.row().classes('w-full h-full justify-between'):
            arrow = utilities.arrow(left_drawer)
            clinicians_search = ui.input(placeholder='Search').classes('border-[#2C25B2] border rounded-md p-1').props('autocomplete="off"').on_value_change(lambda: clinicians_display())

        clinicians_container = ui.row().classes('w-full h-full')
        def clinicians_display():
            filtered_clinicians = clinicians
            if clinicians_search.value:
                filtered_clinicians = [clinician for clinician in clinicians if clinicians_search.value.lower() in (clinician.first_name + ' ' + clinician.last_name).lower()]
            clinicians_container.clear()
            with clinicians_container:
                for clinician in filtered_clinicians:
                    with ui.card().classes('w-full h-full bg-[#F5F5F5] dark:bg-[#1d1d1d] border border-[#2C25B2] no-shadow'):
                        with ui.row().classes(replace='items-center justify-between w-full '):
                            with ui.row().classes('w-full flex justify-between'):
                                with ui.button().classes('px-0').props('flat no-caps color=black align="left"').on_click(partial(navigate_clinician, clinician)):
                                    ui.label(f"{clinician.first_name} {clinician.last_name}").classes('font-bold text-2xl dark:text-white')

                            with ui.row().classes('items-center gap-2 w-full'):
                                with ui.grid(rows=1, columns=2).classes(replace='w-full flex justify-between'):
                                    ui.label(clinician.email).classes('text-xs text-grey')
                                    ui.label(clinician.clinician_id).classes('text-xs text-grey')


        clinicians_display()


