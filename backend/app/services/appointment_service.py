from datetime import datetime, timedelta

from app.database.db import db
from app.database.models import (
    DoctorAvailability,
    Appointment,
    Payment,
    PaymentStatus,
)


APPOINTMENT_FEE = 500  # example fixed fee


def get_alternative_slots(doctor_id, from_time, days=3):
    """Suggest alternative slots for next N days"""
    end_time = from_time + timedelta(days=days)

    slots = (
        DoctorAvailability.query
        .filter(
            DoctorAvailability.doctor_id == doctor_id,
            DoctorAvailability.start_time >= from_time,
            DoctorAvailability.start_time <= end_time,
            DoctorAvailability.is_booked == False
        )
        .order_by(DoctorAvailability.start_time)
        .limit(5)
        .all()
    )

    return [
        {
            "start_time": s.start_time,
            "end_time": s.end_time
        }
        for s in slots
    ]


def book_appointment(patient_id, doctor_id, requested_time):
    # 1️⃣ Check availability
    availability = (
        DoctorAvailability.query
        .filter_by(
            doctor_id=doctor_id,
            start_time=requested_time,
            is_booked=False
        )
        .first()
    )

    if not availability:
        alternatives = get_alternative_slots(
            doctor_id=doctor_id,
            from_time=requested_time
        )

        return {
            "status": "unavailable",
            "message": "Doctor not available at this time",
            "alternatives": alternatives
        }, 409

    # 2️⃣ Book appointment
    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_time=availability.start_time,
        status="scheduled"
    )
    db.session.add(appointment)

    # 3️⃣ Mark slot as booked
    availability.is_booked = True

    db.session.flush()  # get appointment.id

    # 4️⃣ Create payment
    payment = Payment(
        transaction_id=f"TXN-{appointment.id}-{int(datetime.utcnow().timestamp())}",
        user_id=patient_id,
        patient_id=patient_id,
        appointment_id=appointment.id,
        service_details="Doctor Consultation",
        amount=APPOINTMENT_FEE,
        payment_method="online",
        status=PaymentStatus.approved
    )

    db.session.add(payment)
    db.session.commit()

    return {
        "status": "booked",
        "appointment_id": appointment.id,
        "appointment_time": appointment.appointment_time,
        "payment_id": payment.id,
        "amount": payment.amount
    }, 201
