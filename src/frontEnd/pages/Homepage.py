from nicegui import ui, app
import utilities
import UserInformation
import Login
import ActivityPage
import os
import sys

sql_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src', 'backEnd', 'databases', 'SQL'))
if sql_path not in sys.path:
    sys.path.insert(0, sql_path)
try:
    from SQL_read import read_patients_by_clinician_id
except ImportError as e:
    raise ImportError(f"Could not import 'SQL_read'. Make sure 'SQL_read.py' exists in {sql_path}. Original error: {e}")

def header():
    utilities.header()

# creating new page
@ui.page('/main')
def main():
    app.storage.user['current_page'] = '/main'
    # reading in patients
    app.storage.user['patients'] = read_patients_by_clinician_id(app.storage.user.get('clinid'))

    ui.page_title("SocketFit Dashboard")
    genderList = ['All', 'Male', 'Female', 'Prefer not to say']
    amputationTypeList = ['All', 'Above Knee', 'Below Knee', 'Above Elbow', 'Below Elbow']
    app.storage.user['activityList'] = []
    # looping through patients
    for app.storage.user['patient'] in app.storage.user.get('patients'):
        # looping through activities
        for app.storage.user['activity'] in app.storage.user.get('patient').activities:
            app.storage.user['activityList'].append(app.storage.user['activity'])
    header()
    with ui.row().classes('w-full'):
        ui.label("Welcome").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-full'):
        # side tree section
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]'):
            # tree with users needed
           utilities.patients_tree()
        # main section
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            with ui.row().classes('w-full'):
                ui.label("Select User to View Users Information").classes('text-lg font-bold')
                ui.space()
                # box to search users
                search = ui.input(label="Search Name", placeholder='Name', on_change= lambda e: _on_search(e)).classes('border rounded-md border-[#FFB030]')
            ui.label("Filters").classes('text-md font-semibold')

            # filter titles
            with ui.grid(columns=10).classes('w-full gap-4'):
                ui.label("Height (cm):").classes('col-span-2')
                ui.label("Weight (kg):").classes('col-span-2')
                ui.label("Amputation Type:").classes('col-span-2')

            # filter boxes
            with ui.grid(columns=10).classes('w-full gap-4'):

                with ui.row().classes('col-span-2 gap-1'):

                    ui.add_head_html('''
                    <style>
                    input::placeholder {
                        text-align: center;
                    }
                    .q-field__label {
                        text-align: center !important;
                        width: 100% !important;
                    }
                    .q-select .q-field__input {
                        text-align: center !important;
                    }
                    </style>
                    ''')

                    # Height filters with on_change handlers
                    height_min = ui.number(label="Min", placeholder="Min", on_change=lambda e: _on_search(e)).classes('w-2/5 border rounded-md border-[#FFB030]').props('input-style="text-align: center"')
                    height_max = ui.number(label="Max", placeholder="Max", on_change=lambda e: _on_search(e)).classes('w-2/5 border rounded-md border-[#FFB030]').props('input-style="text-align: center"')

                with ui.row().classes('col-span-2 gap-1'):
                    # Weight filters with on_change handlers
                    weight_min = ui.number(label="Min", placeholder="Min", on_change=lambda e: _on_search(e)).classes('w-2/5 border rounded-md border-[#FFB030]').props('input-style="text-align: center"')
                    weight_max = ui.number(label="Max", placeholder="Max", on_change=lambda e: _on_search(e)).classes('w-2/5 border rounded-md border-[#FFB030]').props('input-style="text-align: center"')

                amp_select = ui.select(value=amputationTypeList[0], options=amputationTypeList, on_change= lambda e: _on_search(e)).classes('col-span-2 border rounded-md border-[#FFB030]')

            cards_container = ui.column().classes('w-full')

            def _render_cards(p_list):
                cards_container.clear()
                with cards_container:
                    with ui.grid(columns=4).classes('w-full gap-6'):
                        for p in p_list:
                            full_name = f'{getattr(p, "first_name", "")} {getattr(p, "last_name", "")}'.strip()
                            with ui.card().classes('h-[150px] w-[160px] border border-[#2C25B2] cursor-pointer').on('click', lambda p=p: UserInformation.navigatePatient(p)):
                                ui.label(full_name or "Unnamed").classes('text-xl')
            
            def _filter_by_name(p_list, q):
                q = (q or '').strip().lower()
                if not q:
                    return p_list
                out = []
                for p in p_list:
                    fn = (getattr(p, 'first_name', '') or '').lower()
                    ln = (getattr(p, 'last_name', '') or '').lower()
                    full = f'{fn} {ln}'.strip()
                    if q in fn or q in ln or q in full:
                        out.append(p)
                return out
            
            def _filter_by_amputation(p_list, amp):
                amp = (amp or '').strip().lower()
                if not amp or amp == 'all':
                    return p_list
                out = []
                for p in p_list:
                    a = (getattr(p, 'amputation_type', '') or '').strip().lower()
                    if a == amp:
                        out.append(p)
                return out

            def _filter_by_height(p_list, min_height, max_height):
                out = []
                for p in p_list:
                    height = getattr(p, 'height', None)
                    if height is None:
                        continue
                    
                    # Convert height to number if it's a string
                    try:
                        height = float(height)
                    except (ValueError, TypeError):
                        continue
                    
                    # Check min height
                    if min_height is not None and height < min_height:
                        continue
                    
                    # Check max height
                    if max_height is not None and height > max_height:
                        continue
                    
                    out.append(p)
                return out

            def _filter_by_weight(p_list, min_weight, max_weight):
                out = []
                for p in p_list:
                    weight = getattr(p, 'weight', None)
                    if weight is None:
                        continue
                    
                    # Convert weight to number if it's a string
                    try:
                        weight = float(weight)
                    except (ValueError, TypeError):
                        continue
                    
                    # Check min weight
                    if min_weight is not None and weight < min_weight:
                        continue
                    
                    # Check max weight
                    if max_weight is not None and weight > max_weight:
                        continue
                    
                    out.append(p)
                return out
            
            def _apply_filters():
                base = app.storage.user.get('patients', [])
                
                # Apply name filter
                by_name = _filter_by_name(base, getattr(search, 'value', ''))
                
                # Apply amputation filter
                by_amp = _filter_by_amputation(by_name, getattr(amp_select, 'value', 'All'))
                
                # Apply height filter
                by_height = _filter_by_height(by_amp, getattr(height_min, 'value', None), getattr(height_max, 'value', None))
                
                # Apply weight filter
                by_weight = _filter_by_weight(by_height, getattr(weight_min, 'value', None), getattr(weight_max, 'value', None))
                
                _render_cards(by_weight)

            def _on_search(e):
                _apply_filters()

            _apply_filters()

def mainNavigate():
    ui.navigate.to('/main')

ui.navigate.to('/main')