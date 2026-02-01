from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversation.id"))
    sender = db.Column(db.String(10))  
    text = db.Column(db.Text)
    agent_type = db.Column(db.String(30))  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(50), nullable=False)   
    doctor_id = db.Column(db.Integer, nullable=False)

    patient_name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)

