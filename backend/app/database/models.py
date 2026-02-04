from datetime import datetime
import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    
)
from sqlalchemy.orm import relationship

from .db import db

# ======================
# AUTH & USERS
# ======================


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SystemRole(enum.Enum):
    patient = "patient"
    doctor = "doctor"
    pharmacy = "pharmacy"
    admin = "admin"


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)


class OTP(db.Model):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    code = Column(String)
    purpose = Column(String)  # verify | reset | login
    expires_at = Column(DateTime)
    resend_after = Column(DateTime)


# ======================
# PROFILES
# ======================


class DoctorProfile(db.Model):
    __tablename__ = "doctor_profiles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)

    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=True)

    hospital = db.relationship("Hospital", backref="doctors")


class PatientProfile(db.Model):
    __tablename__ = "patient_profiles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))


class PharmacyProfile(db.Model):
    __tablename__ = "pharmacy_profiles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    store_name = db.Column(db.String(150))
    license_number = db.Column(db.String(50))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    home_delivery_available = db.Column(db.Boolean, default=False)
    self_pickup_available = db.Column(db.Boolean, default=True)

    is_active = db.Column(db.Boolean, default=True)


# ======================
# APPOINTMENTS
# ======================
class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availability"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.user_id"))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    is_booked = db.Column(db.Boolean, default=False)


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient_profiles.user_id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.user_id"))
    appointment_time = db.Column(db.DateTime)
    status = db.Column(db.String(30), default="scheduled")


# ======================
# TELEMEDICINE & CHAT
# ======================


class Consultation(db.Model):
    __tablename__ = "consultations"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey("consultations.id"))
    sender_type = db.Column(db.String(20))  # patient / doctor / ai
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ======================
# MEDICAL RECORDS
# ======================


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient_profiles.user_id"))
    file_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Prescription(db.Model):
    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient_profiles.user_id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.user_id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PrescriptionItem(db.Model):
    __tablename__ = "prescription_items"

    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey("prescriptions.id"))
    medicine_name = db.Column(db.String(100))
    dosage = db.Column(db.String(50))
    duration = db.Column(db.String(50))


# ======================
# HOSPITAL & BEDS
# ======================


class Hospital(db.Model):
    __tablename__ = "hospitals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


class Bed(db.Model):
    __tablename__ = "beds"

    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"))
    bed_type = db.Column(db.String(50))
    is_available = db.Column(db.Boolean, default=True)


# ======================
# EMERGENCY
# ======================


class Ambulance(db.Model):
    __tablename__ = "ambulances"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(50))
    is_available = db.Column(db.Boolean, default=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)


class EmergencyRequest(db.Model):
    __tablename__ = "emergency_requests"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient_profiles.user_id"))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    hospital_id = db.Column(db.Integer, nullable=True)
    ambulance_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(30), default="pending")


# ======================
# PAYMENT AND TRANSCATIONS
# ======================


class PaymentStatus(enum.Enum):
    approved = "approved"
    rejected = "rejected"
    refunded = "refunded"


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    # External / gateway transaction reference
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)

    # Relations
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    patient_id = db.Column(
        db.Integer, db.ForeignKey("patient_profiles.user_id"), nullable=False
    )

    appointment_id = db.Column(
        db.Integer, db.ForeignKey("appointments.id"), nullable=False
    )

    # Payment details
    service_details = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)

    remarks = db.Column(db.Text, nullable=True)

    status = db.Column(
        db.Enum(PaymentStatus), default=PaymentStatus.approved, nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ORM relationships (optional but recommended)
    user = relationship("User")
    patient = relationship("PatientProfile")
    appointment = relationship("Appointment")


def seed_roles():
    from app.database.db import db

    for role in SystemRole:
        exists = Role.query.filter_by(name=role.value).first()
        if not exists:
            db.session.add(Role(name=role.value))

    db.session.commit()


class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)


# class SlotStatus(str, enum.Enum):
#     free = "free"
#     booked = "booked"
#     blocked = "blocked"


# class AppointmentSlot(db.Model):
#     __tablename__ = "appointment_slots"

#     id = Column(Integer, primary_key=True)

#     doctor_id = Column(Integer, ForeignKey("doctors.user_id"))
#     availability_id = Column(Integer, ForeignKey("availability.id"))

#     slot_date = Column(Date)
#     start_time = Column(Time)
#     end_time = Column(Time)

#     status = Column(Enum(SlotStatus), default=SlotStatus.free)

#     created_at = Column(DateTime, default=datetime.utcnow)
#     is_emergency_reserved = Column(Boolean, default=False)


# class Appointment(db.Model):
#     __tablename__ = "appointments"

#     id = Column(Integer, primary_key=True)

#     doctor_id = Column(Integer, ForeignKey("doctors.id"))
#     patient_id = Column(Integer, ForeignKey("patients.id"))
#     slot_id = Column(Integer, ForeignKey("appointment_slots.id"))

#     # appointment_date = Column(Date)
#     # start_time = Column(Time)
#     # end_time = Column(Time)

#     status = Column(String, default="booked")
#     notes = Column(String, nullable=True)

#     created_at = Column(DateTime, default=datetime.utcnow)
#     rescheduled_from_slot = Column(Integer, nullable=True)
#     rescheduled_at = Column(DateTime, nullable=True)

#     cancelled_at = Column(DateTime, nullable=True)
#     cancel_reason = Column(String, nullable=True)
#     cancelled_by = Column(String, nullable=True)  # patient | doctor | admin

#     confirmed = Column(Boolean, default=False)
#     confirmed_at = Column(DateTime, nullable=True)
#     confirmation_notes = Column(String, nullable=True)

#     checked_in = Column(Boolean, default=False)
#     checkin_time = Column(DateTime, nullable=True)
#     attendance_marked_by = Column(String, nullable=True)  # staff | doctor | system

#     consult_mode = Column(Enum(ConsultMode), default=ConsultMode.in_person)

#     is_followup = Column(Boolean, default=False)
#     parent_appointment_id = Column(Integer, nullable=True)
#     followup_reason = Column(String, nullable=True)

#     is_emergency = Column(Boolean, default=False)
#     emergency_reason = Column(String, nullable=True)


# class AppointmentStatusLog(db.Model):
#     __tablename__ = "appointment_status_logs"

#     id = Column(Integer, primary_key=True)

#     appointment_id = Column(Integer, ForeignKey("appointments.id"))

#     old_status = Column(String)
#     new_status = Column(String)

#     changed_by = Column(String)   # system | doctor | patient | admin
#     reason = Column(String, nullable=True)

#     changed_at = Column(DateTime, default=datetime.utcnow)

# class NotificationLog(db.Model):
#     __tablename__ = "notification_logs"

#     id = Column(Integer, primary_key=True)

#     appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)

#     recipient = Column(String)   # email or phone
#     channel = Column(String)     # email | whatsapp
#     type = Column(String)        # reminder | confirm | cancel

#     message = Column(String)

#     scheduled_for = Column(DateTime)
#     sent_at = Column(DateTime, nullable=True)

#     status = Column(String, default="pending")  # pending/sent/failed

# import enum

# class ConsultMode(str, enum.Enum):
#     in_person = "in_person"
#     video = "video"
#     audio = "audio"
#     chat = "chat"

# class VideoSession(db.Model):
#     __tablename__ = "video_sessions"

#     id = Column(Integer, primary_key=True)

#     appointment_id = Column(Integer, ForeignKey("appointments.id"))

#     room_name = Column(String, unique=True)
#     doctor_join_url = Column(String)
#     patient_join_url = Column(String)

#     created_at = Column(DateTime, default=datetime.utcnow)
#     expires_at = Column(DateTime)

# class MedicalRecord(db.Model):
#     __tablename__ = "medical_records"

#     id = Column(Integer, primary_key=True)

#     appointment_id = Column(Integer, ForeignKey("appointments.id"))
#     doctor_id = Column(Integer, ForeignKey("doctors.id"))
#     patient_id = Column(Integer, ForeignKey("patients.id"))

#     notes_text = Column(String, nullable=True)
#     diagnosis = Column(String, nullable=True)
#     prescription_text = Column(String, nullable=True)

#     file_path = Column(String, nullable=True)

#     created_at = Column(DateTime, default=datetime.utcnow)

# class Role(db.Model):
#     __tablename__ = "roles"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True)

# class AuditLog(db.Model):
#     __tablename__ = "audit_logs"

#     id = Column(Integer, primary_key=True)

#     actor_user = Column(String)
#     actor_role = Column(String)

#     action = Column(String)
#     entity_type = Column(String)
#     entity_id = Column(Integer)

#     old_values = Column(String, nullable=True)
#     new_values = Column(String, nullable=True)

#     ip_address = Column(String, nullable=True)

#     created_at = Column(DateTime, default=datetime.utcnow)

# class Feedback(db.Model):
#     __tablename__ = "feedback"

#     id = Column(Integer, primary_key=True)

#     appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True)
#     doctor_id = Column(Integer, ForeignKey("doctors.id"))
#     patient_id = Column(Integer, ForeignKey("patients.id"))

#     rating = Column(Integer)  # 1–5
#     comments = Column(String, nullable=True)

#     created_at = Column(DateTime, default=datetime.utcnow)


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    user_id = Column(db.Integer, ForeignKey("users.id"))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"))
    sender = db.Column(db.String(10))
    text = db.Column(db.Text)
    # agent_type = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# class Hospital(db.Model):
#     __tablename__ = "hospitals"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     address = Column(String)
#     latitude = Column(String)
#     longitude = Column(String)

# class Bed(db.Model):
#     __tablename__ = "beds"

#     id = Column(Integer, primary_key=True)
#     hospital_id = Column(Integer, ForeignKey("hospitals.id"))
#     bed_type = Column(String)     # ICU, General, Ventilator
#     is_available = Column(Boolean, default=True)


# class Ambulance(db.Model):
#     __tablename__ = "ambulances"

#     id = Column(Integer, primary_key=True)
#     vehicle_number = Column(String, unique=True)
#     is_available = Column(Boolean, default=True)

# class EmergencyRequest(db.Model):
#     __tablename__ = "emergency_requests"

#     id = Column(Integer, primary_key=True)
#     patient_id = Column(Integer, ForeignKey("patients.id"))
#     latitude = Column(String)
#     longitude = Column(String)
#     status = Column(String, default="pending")


# class Prescription(db.Model):
#     __tablename__ = "prescriptions"

#     id = Column(Integer, primary_key=True)
#     appointment_id = Column(Integer, ForeignKey("appointments.id"))
#     created_at = Column(DateTime, default=datetime.utcnow)

# class PrescriptionItem(db.Model):
#     __tablename__ = "prescription_items"

#     id = Column(Integer, primary_key=True)
#     prescription_id = Column(Integer, ForeignKey("prescriptions.id"))
#     medicine_name = Column(String)
#     dosage = Column(String)
#     duration = Column(String)
