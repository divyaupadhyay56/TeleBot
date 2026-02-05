import os
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def save_prescription_file(file, appointment_id):
    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()

    new_filename = f"appointment_{appointment_id}.{ext}"
    upload_path = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_path, exist_ok=True)
    full_path = os.path.join(upload_path, new_filename)

    file.save(full_path)

    return full_path, ext
