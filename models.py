from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer)
    sender = db.Column(db.String(20))  # user / bot
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialization = db.Column(db.String(50))
    city = db.Column(db.String(50))
    contact = db.Column(db.String(20))

# ✅ NEW TABLE
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(50), nullable=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    doctor = db.relationship("Doctor", backref="appointments")

    date = db.Column(db.String(20), nullable=False)  # "2026-01-25"
    time = db.Column(db.String(20), nullable=False)  # "11:30"

    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="scheduled")  # scheduled/cancelled/completed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
