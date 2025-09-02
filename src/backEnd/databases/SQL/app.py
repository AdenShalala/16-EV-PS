from flask import Flask, jsonify, request
from flask_cors import CORS  
from SQL_read import read_patients_by_clinician_id
import os
import math
from typing import Any

app = Flask(__name__)
# if cross fields, uncomment the next line
CORS(app)  # CORS(app, resources={r"/*": {"origins": "*"}})

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


def to_serializable(obj: Any):
    
    # normal types
    if obj is None or isinstance(obj, (bool, int, float, str)):
        # NaN/inf, weird error
        if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
            return None
        return obj

    # list, tuple, set
    if isinstance(obj, (list, tuple, set)):
        return [to_serializable(x) for x in obj]

    # dictionary
    if isinstance(obj, dict):
        return {str(k): to_serializable(v) for k, v in obj.items()}

    # other objects, try __dict__ / vars()
    try:
        d = vars(obj)
    except TypeError:
        
        return str(obj)

    # deal with attributes
    return {k: to_serializable(v) for k, v in d.items()}


@app.get("/patients/<string:clinician_id>")
def get_patients(clinician_id: str):
    
    #base on clinician_id get the Patient objects（including activities, sensors etc.），return JSON.
    #call SQL_read.read_patients_by_clinician_id(clinician_id)
    
    try:
        patients = read_patients_by_clinician_id(clinician_id)
    
        data = to_serializable(patients if patients is not None else [])
        return jsonify({"clinician_id": clinician_id, "count": len(data), "patients": data}), 200
    except Exception as e:
  
        return jsonify({"error": "internal_error", "detail": str(e)}), 500



if __name__ == "__main__":

    port = int(os.getenv("PORT", "5000"))

    app.run(host="0.0.0.0", port=port, debug=True)
