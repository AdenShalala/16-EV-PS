# from nicegui import ui, app
# import api
# import pages.login

# pages.login.create()

# ui.run_with(app=api.app, storage_secret="tuehauhd")

from fastapi import FastAPI
from nicegui import app as nicegui_app, ui
import pages.login
import oldapi
import database
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Request
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from schema import *

app = FastAPI()


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not nicegui_app.storage.user.get('token', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path != '/test':
                return RedirectResponse(f'/login?redirect_to={request.url.path}')
        return await call_next(request)
    
nicegui_app.add_middleware(AuthMiddleware)

pages.login.create()




# @app.get('/')
# def read_root():
#     session, token = api.create_session()
#     #print(session)
#     print(api.validate_token(token))
#     database.delete_session(session.session_id)
#     return {'Hello': 'World'}

oldapi.login = app.get('/login')

# Integrate with your FastAPI Application
ui.run_with(
    app=app,
    storage_secret='pick your private secret here',
)