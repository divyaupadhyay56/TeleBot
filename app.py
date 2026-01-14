from flask import Flask
from Chatbot.models import db
from Chatbot.routes.sync import sync_bp
from Chatbot.routes.chatbot import chatbot_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register blueprints
app.register_blueprint(sync_bp)
app.register_blueprint(chatbot_bp)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"status": "Flask backend running", "service": "Chatbot API"}

if __name__ == "__main__":
    # IMPORTANT: Run with module mode, not direct file mode
    app.run(debug=True)
