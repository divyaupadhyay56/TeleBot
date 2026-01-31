from flask import Flask
from TeleBot.config import DevelopmentConfig
from TeleBot.models import db
from TeleBot.routes.chatbot import chatbot_bp
from TeleBot.routes.appointment import appointment_bp
from TeleBot.routes.sync import sync_bp   # 🔥 ADD THIS

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(chatbot_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(sync_bp)   # 🔥 REGISTER HERE

    @app.route("/")
    def home():
        return {
            "service": "TeleBot Backend",
            "routes": [
                "/chat",
                "/sync",
                "/doctors",
                "/appointment"
            ]
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
