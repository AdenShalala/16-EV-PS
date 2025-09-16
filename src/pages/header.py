from nicegui import ui
import os

def header():
    with ui.header().style('background-color: #FFFFFF'):
        with ui.row().classes('w-full justify-center items-center'):
            ui.image(os.path.join("src", "assets", "dashboard.png")).classes('h-[40px] w-[140px]')