from app.database.models import JanaushadhiKendra
from app.utils.geo_utils import haversine


def find_nearby_kendras(lat, lng, radius_km=5):
    kendras = JanaushadhiKendra.query.filter(
        JanaushadhiKendra.latitude.isnot(None),
        JanaushadhiKendra.longitude.isnot(None)
    ).all()

    results = []

    for k in kendras:
        distance = haversine(
            lat, lng,
            k.latitude, k.longitude
        )

        if distance <= radius_km:
            results.append({
                "name": k.name,
                "kendra_code": k.kendra_code,
                "address": k.address,
                "district": k.district_name,
                "state": k.state_name,
                "pin_code": k.pin_code,
                "distance_km": round(distance, 2),
                "location": {
                    "lat": k.latitude,
                    "lng": k.longitude
                }
            })

    return sorted(results, key=lambda x: x["distance_km"])
