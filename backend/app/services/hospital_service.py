from app.database.models import Hospital
from app.database.db import db

def get_all_hospitals():
    hospitals = Hospital.query.all()

    return [
        {
            "id": h.id,
            "name": h.name,
            "latitude": h.latitude,
            "longitude": h.longitude,
        }
        for h in hospitals
    ]


def get_hospital_by_id(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        return None

    return {
        "id": hospital.id,
        "name": hospital.name,
        "latitude": hospital.latitude,
        "longitude": hospital.longitude,
    }


def create_hospital(data):
    hospital = Hospital(
        name=data.get("name"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude")
    )

    db.session.add(hospital)
    db.session.commit()

    return {
        "id": hospital.id,
        "name": hospital.name,
        "latitude": hospital.latitude,
        "longitude": hospital.longitude
    }