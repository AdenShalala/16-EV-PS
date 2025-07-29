import os
from flask import Flask, jsonify, abort
from dotenv import load_dotenv
from SQL_read import read_patients_by_clinician_id
from Patient import Patient
from Activity import Activity
from Sensor import Sensor

load_dotenv()


app = Flask(__name__)

@app.route('/clinicians/<string:clinician_id>/patients', methods=['GET'])
def get_patients(clinician_id):
    """
    call SQL_read.read_patients_by_clinician_id，
    return objects
    """
    patients = read_patients_by_clinician_id(clinician_id)
    if not patients:
        abort(404, description=f'Clinician {clinician_id} has no patients or does not exist')
    
    result = []
    for p in patients:
        pd = p.__dict__.copy()
        # activities is list[Activity]
        pd['activities'] = []
        for a in p.activities:
            ad = a.__dict__.copy()
            # sensors is list[Sensor]
            ad['sensors'] = [s.__dict__ for s in a.sensors]
            pd['activities'].append(ad)
        result.append(pd)
    return jsonify(result), 200

@app.errorhandler(404)
def handle_404(error):
    return jsonify({'error': error.description}), 404

if __name__ == '__main__':
    # .env:
    # MYSQL_HOST=127.0.0.1
    # MYSQL_PORT=3306
    # MYSQL_USER=root
    # MYSQL_PASSWORD=2233
    # MYSQL_DATABASE=testdb
    # FLASK_RUN_PORT=5000
    # FLASK_DEBUG=true
    port  = int(os.getenv('FLASK_RUN_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
