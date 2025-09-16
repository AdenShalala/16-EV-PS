# from nicegui import ui, app
# import api
# import pages.login

# pages.login.create()

# ui.run_with(app=api.app, storage_secret="tuehauhd")

from fastapi import FastAPI
from nicegui import app as nicegui_app, ui

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


# Integrate with your FastAPI Application
ui.run_with(
    app=app,
    storage_secret='pick your private secret here',
)