from app.database.db import db
from app.database.models import Prescription
from app.utils.file_utils import allowed_file, save_prescription_file


def upload_prescription(file, appointment_id, patient_id, doctor_id):
    if not file or file.filename == "":
        return {"error": "No file provided"}, 400

    if not allowed_file(file.filename):
        return {"error": "Invalid file type"}, 400

    file_path, file_type = save_prescription_file(file, appointment_id)

    prescription = Prescription(
        appointment_id=appointment_id,
        patient_id=patient_id,
        doctor_id=doctor_id,
        file_path=file_path,
        file_type=file_type,
    )

    db.session.add(prescription)
    db.session.commit()

    return {
        "message": "Prescription uploaded successfully",
        "prescription_id": prescription.id,
    }, 201
