from flask import Flask
from dotenv import load_dotenv
import os

from TeleBot.models import db
from config import DevelopmentConfig

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    # register blueprints here
    from TeleBot.routes.appointment import appointment_bp
    from TeleBot.routes.chatbot import chatbot_bp
    from TeleBot.routes.seed import seed_bp
    from TeleBot.routes.sync import sync_bp

    app.register_blueprint(appointment_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(seed_bp)
    app.register_blueprint(sync_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
