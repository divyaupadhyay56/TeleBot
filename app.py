from flask import Flask
from TeleBot.config import DevelopmentConfig
from TeleBot.models import db
from TeleBot.routes.chatbot import chatbot_bp
from TeleBot.routes.appointment import appointment_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    app.register_blueprint(chatbot_bp)
    app.register_blueprint(appointment_bp)

    @app.route("/")
    def home():
        return {
            "service": "TeleBot Backend",
            "options": ["Talk to AI", "Talk to Doctor"]
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
