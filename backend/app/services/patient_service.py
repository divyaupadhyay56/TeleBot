from app.database.models import PatientProfile, User

def get_all_patients():
    patients = (
        PatientProfile.query
        .join(User, User.id == PatientProfile.user_id)
        .all()
    )

    return [
        {
            "user_id": p.user_id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "blood_group": p.blood_group,
        }
        for p in patients
    ]


def get_patient_by_id(user_id):
    patient = (
        PatientProfile.query
        .filter(PatientProfile.user_id == user_id)
        .first()
    )

    if not patient:
        return None

    return {
        "user_id": patient.user_id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "blood_group": patient.blood_group,
    }
