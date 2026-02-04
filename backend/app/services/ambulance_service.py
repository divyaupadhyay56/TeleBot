from app.database.models import Ambulance, EmergencyRequest
from app.database.db import db
from app.utils.geo_utils import haversine


def call_ambulance(patient_id, lat, lng):
    ambulances = Ambulance.query.filter_by(is_available=True).all()
    if not ambulances:
        return {"error": "No ambulance available"}, 409

    nearest = min(
        ambulances, key=lambda a: haversine(lat, lng, a.latitude, a.longitude)
    )

    nearest.is_available = False

    emergency = EmergencyRequest(
        patient_id=patient_id,
        latitude=lat,
        longitude=lng,
        ambulance_id=nearest.id,
        status="ambulance_dispatched",
    )

    db.session.add(emergency)
    db.session.commit()

    return {
        "status": "ok",
        "ambulance": {"id": nearest.id, "vehicle_number": nearest.vehicle_number},
    }
