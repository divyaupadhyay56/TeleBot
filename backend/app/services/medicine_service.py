from app.database.models import PharmacyInventory, PharmacyProfile
from app.utils.geo_utils import haversine


def search_medicine(medicine_name, user_lat, user_lng, radius_km=5):
    medicine_name = medicine_name.lower()

    inventories = PharmacyInventory.query.filter(
        PharmacyInventory.medicine_name.ilike(f"%{medicine_name}%"),
        PharmacyInventory.quantity > 0,
        PharmacyInventory.is_active == True,
    ).all()

    results = []

    for inv in inventories:
        pharmacy = PharmacyProfile.query.filter_by(
            user_id=inv.pharmacy_id, is_active=True
        ).first()

        if not pharmacy:
            continue

        distance = haversine(user_lat, user_lng, pharmacy.latitude, pharmacy.longitude)

        if distance <= radius_km:
            results.append(
                {
                    "pharmacy_id": pharmacy.user_id,
                    "store_name": pharmacy.store_name,
                    "medicine_name": inv.medicine_name,
                    "available_quantity": inv.quantity,
                    "distance_km": round(distance, 2),
                    "home_delivery_available": pharmacy.home_delivery_available,
                    "self_pickup_available": pharmacy.self_pickup_available,
                    "location": {"lat": pharmacy.latitude, "lng": pharmacy.longitude},
                }
            )

    return sorted(results, key=lambda x: x["distance_km"])
