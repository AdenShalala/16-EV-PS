from nicegui import ui, app
import requests
from src.pages.utilities import header


def create() -> None:
    @ui.page('/')
    def root():
        def logout() -> None:
            app.storage.user.clear()
            ui.navigate.to('/login')

        with ui.column().classes('absolute-center items-center'):
            ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
            ui.button(on_click=logout, icon='logout').props('outline round')