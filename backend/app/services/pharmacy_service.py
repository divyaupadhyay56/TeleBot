from app.database.models import PharmacyProfile

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


def get_pharmacy_by_id(user_id):
    pharmacy = PharmacyProfile.query.filter_by(user_id=user_id).first()
    if not pharmacy:
        return None

    return {
        "user_id": pharmacy.user_id,
        "store_name": pharmacy.store_name,
        "license_number": pharmacy.license_number,
    }
