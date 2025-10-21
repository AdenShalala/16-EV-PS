
from nicegui import ui, app, events
import pages.utilities as utilities
import api
from functools import partial
import xml_util
from starlette.formparsers import MultiPartParser
import threading

from tqdm import tqdm

MultiPartParser.spool_max_size = 1024 * 1024 * 5  



def navigate_clinician(clinician):
    app.storage.user['selected_clinician'] = clinician.clinician_id
    ui.navigate.to("/clinician")

def create() -> None:
    @ui.page('/settings')
    def settings():
        app.storage.user['current_page'] = '/settings'
        ui.page_title('SocketFit Admin')
        utilities.header()
        left_drawer = utilities.admin_sidebar()
        utilities.arrow(left_drawer)

        with ui.row().classes(' w-full flex justify-center'):
            with ui.card().classes('w-1/2 justify-center items-center bg-[#F5F5F5] dark:bg-[#1d1d1d] border border-[#2C25B2] no-shadow'):
                ui.label("Generate XML").classes('font-bold text-xl dark:text-white')    

                def generate_xml():
                    xml = xml_util.generate()
                    
                    ui.download.content(xml[0] + xml[1] + xml[2], 'generated_data.xml')

                ui.button('Download XML', color='#FFB030', on_click=lambda: generate_xml()).classes('text-white')

                ui.separator()

                ui.label("Upload XML").classes('font-bold text-xl dark:text-white')    

                async def handle_upload(e: events.UploadEventArguments):
                    x = e.content.read().decode('utf-8')
                    
                    def read_thread(x):
                        thread = threading.Thread(target=xml_util.read, args=x)
                        thread.start()

                ui.upload(on_upload=handle_upload, max_file_size=10_485_760).props('accept=.xml').classes('max-w-full flat').style('--q-primary: #FFB030')

                



            
