from flask import Flask
from Chatbot.models import db
from Chatbot.routes.sync import sync_bp
from Chatbot.routes.chatbot import chatbot_bp
from Chatbot.routes.appointment import appointment_bp
from Chatbot.routes.seed import seed_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ✅ Register blueprints
app.register_blueprint(sync_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(seed_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"status": "Flask backend running", "service": "Chatbot API"}

# ✅ Mode selector (2 options)
@app.route("/options")
def options():
    return {
        "status": "success",
        "options": [
            {"mode": "ai", "title": "Talk to AI Chatbot", "endpoint": "/chat"},
            {"mode": "doctor", "title": "Talk to Doctor", "endpoint": "/doctors"}
        ]
    }

if __name__ == "__main__":
    app.run(debug=True)

