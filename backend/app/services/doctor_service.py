from app.database.models import DoctorProfile, User

def get_all_doctors():
    doctors = (
        DoctorProfile.query
        .join(User, User.id == DoctorProfile.user_id)
        .all()
    )

    return [
        {
            "user_id": d.user_id,
            "name": d.name,
            "specialization": d.specialization,
            "experience_years": d.experience_years,
        }
        for d in doctors
    ]


def get_doctor_by_id(user_id):
    doctor = (
        DoctorProfile.query
        .join(User, User.id == DoctorProfile.user_id)
        .filter(DoctorProfile.user_id == user_id)
        .first()
    )

    if not doctor:
        return None

    return {
        "user_id": doctor.user_id,
        "name": doctor.name,
        "specialization": doctor.specialization,
        "experience_years": doctor.experience_years,
    }
