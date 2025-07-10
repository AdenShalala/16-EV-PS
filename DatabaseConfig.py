from nicegui import ui
import elements
import WriteFromFile

def header():
    elements.header()

@ui.page('/config')
def config():
    ui.page_title("SocketFit Dashboard")
    header()
    with ui.row().classes('w-full'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]') as patients:
            ui.label("Database Configuration")
            ui.label("Write to Database From File")
        with ui.card().classes('w-3/4 border rounded-md border-[#2C25B2] justify-center items-center') as main:
            # ui.input("Database Choice").classes('border rounded-md border-[#2C25B2]')
            
            def handle_database_upload(e):
                content = e.content.read().decode('utf-8')
                print("Uploaded content:", content)
                ui.notify(f'File "{e.name}" uploaded successfully!')
                

            ui.upload(
                label='Drag and drop or browse for Datebase',
                on_upload=handle_database_upload,
                auto_upload=True,
                max_files=1,
            ).props('accept=".xml"').style('color: #3545FF; text-transform: none;').classes('rounded-md px-4 py-2')
            # ui.button("Browse computer for files", color="#FFB030", on_click= upload_txt_file()) 
            ui.input(placeholder='Height Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Weight Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Age Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Gender Column Name Here...').classes('border rounded-md border-[#3545FF]')
    ui.button('next', on_click=WriteFromFile.navigateFile)

def navigateConfig():
    ui.navigate.to('/config')

ui.run()
ui.navigate.to('/config')