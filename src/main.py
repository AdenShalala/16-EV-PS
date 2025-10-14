from nicegui import app as app, ui
import os
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
import sessions

import pages.login as login
import pages.root as root
import pages.admin as admin
import pages.clinician as clinician
import pages.patient as patient
import pages.session as session_page
import pages.activity as activity

load_dotenv()

class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('token', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path != "/login":
                return RedirectResponse('/login')
        else:
            s = sessions.validate_session(token=app.storage.user.get('token'))
            
            if s == None:
                app.storage.user.clear()

            if s.account_type == "Admin":
                # redirect if admin
                if not request.url.path.startswith('/_nicegui') and not request.url.path.startswith('/admin'):
                    return RedirectResponse('/admin')
            else:
                # redirect if not admin
                if not request.url.path.startswith('/_nicegui') and request.url.path.startswith('/admin'):
                    return RedirectResponse('/')
                
        return await call_next(request)


app.add_middleware(AuthMiddleware)


login.create()
root.create()
admin.create()
clinician.create()
patient.create()
session_page.create()
activity.create()

app.add_static_files('/assets', 'src/assets')
ui.run(storage_secret=os.getenv("STORAGE_SECRET"), favicon="src/assets/favicon.ico")