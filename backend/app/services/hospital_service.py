from app.database.models import Hospital

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
