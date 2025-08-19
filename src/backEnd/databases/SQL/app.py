from flask import Flask, jsonify, request
from flask_cors import CORS
from SQL_read import read_patients_by_clinician_id
import os
import math
from typing import Any

app = Flask(__name__)
CORS(app)  # frontend testing


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


def to_serializable(obj: Any):
    """Convert Patient/Activity/Sensor objects (or nested structures) into JSON-serializable dicts."""
    if obj is None or isinstance(obj, (bool, int, float, str)):
        if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
            return None
        return obj

    if isinstance(obj, (list, tuple, set)):
        return [to_serializable(x) for x in obj]

    if isinstance(obj, dict):
        return {str(k): to_serializable(v) for k, v in obj.items()}

    try:
        d = vars(obj)
    except TypeError:
        return str(obj)

    return {k: to_serializable(v) for k, v in d.items()}


@app.get("/patients/<string:clinician_id>")
def get_patients(clinician_id: str):
    """
    Get all patients assigned to a given clinician_id (including activities and sensors).
    Uses SQL_read.read_patients_by_clinician_id(clinician_id).
    """
    try:
        patients = read_patients_by_clinician_id(clinician_id)
        data = to_serializable(patients if patients is not None else [])
        return jsonify({"clinician_id": clinician_id, "count": len(data), "patients": data}), 200
    except Exception as e:
        return jsonify({"error": "internal_error", "detail": str(e)}), 500


# support query parameter style ?clinician_id=CLIN402
@app.get("/patients")
def get_patients_query():
    clinician_id = request.args.get("clinician_id", type=str)
    if not clinician_id:
        return jsonify({"error": "missing_parameter", "detail": "clinician_id is required"}), 400
    try:
        patients = read_patients_by_clinician_id(clinician_id)
        data = to_serializable(patients if patients is not None else [])
        return jsonify({"clinician_id": clinician_id, "count": len(data), "patients": data}), 200
    except Exception as e:
        return jsonify({"error": "internal_error", "detail": str(e)}), 500


@app.get("/")
def index():
    return jsonify({
        "endpoints": [
            {"GET": "/health"},
            {"GET": "/patients/<clinician_id>"},
            {"GET": "/patients?clinician_id=..."}
        ]
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
