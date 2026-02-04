from app.database.models import PharmacyProfile
from app.utils.geo_utils import haversine


def get_all_pharmacies():
    pharmacies = PharmacyProfile.query.all()

    return [
        {
            "user_id": p.user_id,
            "store_name": p.store_name,
            "license_number": p.license_number,
        }
        for p in pharmacies
    ]


# def get_pharmacy_by_id(user_id):
#     pharmacy = PharmacyProfile.query.filter_by(user_id=user_id).first()
#     if not pharmacy:
#         return None

#     return {
#         "user_id": pharmacy.user_id,
#         "store_name": pharmacy.store_name,
#         "license_number": pharmacy.license_number,
#     }


def get_pharmacy_profile(user_id):
    pharmacy = PharmacyProfile.query.filter_by(user_id=user_id, is_active=True).first()

    if not pharmacy:
        return None

    return {
        "user_id": pharmacy.user_id,
        "store_name": pharmacy.store_name,
        "license_number": pharmacy.license_number,
        "location": {"lat": pharmacy.latitude, "lng": pharmacy.longitude},
        "home_delivery_available": pharmacy.home_delivery_available,
        "self_pickup_available": pharmacy.self_pickup_available,
    }


def find_nearby_pharmacies(lat, lng, radius_km=5):
    pharmacies = PharmacyProfile.query.filter_by(is_active=True).all()
    results = []

    for p in pharmacies:
        distance = haversine(lat, lng, p.latitude, p.longitude)
        if distance <= radius_km:
            results.append(
                {
                    "user_id": p.user_id,
                    "store_name": p.store_name,
                    "distance_km": round(distance, 2),
                    "location": {"lat": p.latitude, "lng": p.longitude},
                    "home_delivery_available": p.home_delivery_available,
                    "self_pickup_available": p.self_pickup_available,
                }
            )

    return sorted(results, key=lambda x: x["distance_km"])
