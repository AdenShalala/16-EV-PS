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
import pages.dashboard as dashboard
import pages.account as account
import pages.settings as settings

load_dotenv()

admin_pages = {'/admin', '/clinician', 'settings', '/docs'}
clinician_pages = {'/dashboard', '/patient', '/'}

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
                if not request.url.path.startswith('/_nicegui') and request.url.path in clinician_pages:
                    return RedirectResponse('/admin')
            else:
                # redirect if not admin
                if not request.url.path.startswith('/_nicegui') and request.url.path in admin_pages:
                    return RedirectResponse('/')
                
        return await call_next(request)


app.add_middleware(AuthMiddleware)
from argon2 import PasswordHasher

login.create()
root.create()
admin.create()
clinician.create()
patient.create()
dashboard.create()
account.create()
settings.create()

ph = PasswordHasher()

app.add_static_files('/assets', 'src/assets')
ui.run(storage_secret=os.getenv("STORAGE_SECRET"), favicon="src/assets/favicon.png", fastapi_docs=True)