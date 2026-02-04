from app.database.models import Hospital, EmergencyRequest
from app.database.db import db
from app.utils.geo_utils import haversine


def handle_emergency(patient_id, lat, lng):
    hospitals = Hospital.query.all()
    if not hospitals:
        return {"error": "No hospitals registered"}, 500

    nearest = min(hospitals, key=lambda h: haversine(lat, lng, h.latitude, h.longitude))

    emergency = EmergencyRequest(
        patient_id=patient_id,
        latitude=lat,
        longitude=lng,
        hospital_id=nearest.id,
        status="sent_to_hospital",
    )

    db.session.add(emergency)
    db.session.commit()

    return {"status": "ok", "hospital": {"id": nearest.id, "name": nearest.name}}
