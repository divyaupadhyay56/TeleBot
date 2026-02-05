from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.models import Prescription
from app.services.prescription_service import upload_prescription

prescription_bp = Blueprint("prescriptions", __name__, url_prefix="/prescriptions")


# 🔼 Upload prescription (Doctor only)
@prescription_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    appointment_id = request.form.get("appointment_id")
    patient_id = request.form.get("patient_id")
    file = request.files.get("file")

    if not appointment_id or not patient_id:
        return {"error": "appointment_id and patient_id required"}, 400

    doctor_id = get_jwt_identity()

    return upload_prescription(
        file=file,
        appointment_id=appointment_id,
        patient_id=patient_id,
        doctor_id=doctor_id,
    )


# 🔽 Download prescription
@prescription_bp.route("/<int:prescription_id>/download", methods=["GET"])
@jwt_required()
def download(prescription_id):
    user_id = get_jwt_identity()

    prescription = Prescription.query.get_or_404(prescription_id)

    # 🔒 Authorization check
    if user_id not in [prescription.patient_id, prescription.doctor_id]:
        return {"error": "Unauthorized"}, 403

    return send_file(prescription.file_path, as_attachment=True)
