
from nicegui import ui, app
import os, sys
#import ClinicianInformation
import pages.utilities as utilities
import api
from schema import Clinician


def create() -> None:
    @ui.page('/admin')
    def admin():
        app.storage.user['current_page'] = '/admin'
        ui.page_title('SocketFit Admin')
        utilities.header()
        left_drawer = utilities.admin_sidebar()
        utilities.arrow(left_drawer)
        



