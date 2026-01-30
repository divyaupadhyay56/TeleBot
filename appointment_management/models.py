from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date
from database import Base
from datetime import datetime
from sqlalchemy import ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship

from sqlalchemy import Enum
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    password_hash = Column(String)
    verified = Column(Boolean, default=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")


class OTP(Base):
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    code = Column(String)
    purpose = Column(String)  # verify | reset | login
    expires_at = Column(DateTime)
    resend_after = Column(DateTime)

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)

    specialization = Column(String)
    experience_years = Column(Integer)
    hospital = Column(String)
    bio = Column(String)

    profile_photo_url = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    supported_modes = Column(String, default="in_person,video")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)

    date_of_birth = Column(Date)
    gender = Column(String)
    blood_group = Column(String)

    address = Column(String)
    emergency_contact = Column(String)
    medical_notes = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    day_of_week = Column(Integer)  # 0=Mon ... 6=Sun
    date = Column(Date, nullable=True)

    start_time = Column(Time)
    end_time = Column(Time)

    slot_minutes = Column(Integer, default=30)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    doctor = relationship("Doctor")


class SlotStatus(str, enum.Enum):
    free = "free"
    booked = "booked"
    blocked = "blocked"


class AppointmentSlot(Base):
    __tablename__ = "appointment_slots"

    id = Column(Integer, primary_key=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    availability_id = Column(Integer, ForeignKey("availability.id"))

    slot_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    status = Column(String, default="free")

    created_at = Column(DateTime, default=datetime.utcnow)
    is_emergency_reserved = Column(Boolean, default=False)



class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    slot_id = Column(Integer, ForeignKey("appointment_slots.id"))

    appointment_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    status = Column(String, default="booked")
    notes = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    rescheduled_from_slot = Column(Integer, nullable=True)
    rescheduled_at = Column(DateTime, nullable=True)

    cancelled_at = Column(DateTime, nullable=True)
    cancel_reason = Column(String, nullable=True)
    cancelled_by = Column(String, nullable=True)  # patient | doctor | admin

    confirmed = Column(Boolean, default=False)
    confirmed_at = Column(DateTime, nullable=True)
    confirmation_notes = Column(String, nullable=True)

    checked_in = Column(Boolean, default=False)
    checkin_time = Column(DateTime, nullable=True)
    attendance_marked_by = Column(String, nullable=True)  # staff | doctor | system

    consult_mode = Column(String, default="in_person")

    is_followup = Column(Boolean, default=False)
    parent_appointment_id = Column(Integer, nullable=True)
    followup_reason = Column(String, nullable=True)

    is_emergency = Column(Boolean, default=False)
    emergency_reason = Column(String, nullable=True)


class AppointmentStatusLog(Base):
    __tablename__ = "appointment_status_logs"

    id = Column(Integer, primary_key=True)

    appointment_id = Column(Integer, ForeignKey("appointments.id"))

    old_status = Column(String)
    new_status = Column(String)

    changed_by = Column(String)   # system | doctor | patient | admin
    reason = Column(String, nullable=True)

    changed_at = Column(DateTime, default=datetime.utcnow)

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True)

    appointment_id = Column(Integer, nullable=True)

    recipient = Column(String)   # email or phone
    channel = Column(String)     # email | whatsapp
    type = Column(String)        # reminder | confirm | cancel

    message = Column(String)

    scheduled_for = Column(DateTime)
    sent_at = Column(DateTime, nullable=True)

    status = Column(String, default="pending")  # pending/sent/failed

import enum

class ConsultMode(str, enum.Enum):
    in_person = "in_person"
    video = "video"
    audio = "audio"
    chat = "chat"

class VideoSession(Base):
    __tablename__ = "video_sessions"

    id = Column(Integer, primary_key=True)

    appointment_id = Column(Integer, ForeignKey("appointments.id"))

    room_name = Column(String, unique=True)
    doctor_join_url = Column(String)
    patient_join_url = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True)

    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

    notes_text = Column(String, nullable=True)
    diagnosis = Column(String, nullable=True)
    prescription_text = Column(String, nullable=True)

    file_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    actor_user = Column(String)
    actor_role = Column(String)

    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(Integer)

    old_values = Column(String, nullable=True)
    new_values = Column(String, nullable=True)

    ip_address = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)

    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

    rating = Column(Integer)  # 1–5
    comments = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

