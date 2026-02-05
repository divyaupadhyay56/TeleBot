from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database.db import db
from app.database.models import Conversation, Message
from app.services.ai_engine import analyze_symptoms
from app.services.context_manager import build_context

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")


@chatbot_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    try:
        data = request.get_json()

        user_id = get_jwt_identity()
        text = str(data.get("message", "")).strip()
        agent_type = data.get("agent_type", "medical_ai")

        if not text:
            return jsonify({"error": "Message required"}), 400

        # 1️⃣ Find or create conversation
        convo = Conversation.query.filter_by(user_id=user_id).first()
        if not convo:
            convo = Conversation(user_id=user_id)
            db.session.add(convo)
            db.session.commit()

        # 2️⃣ Save user message
        db.session.add(Message(conversation_id=convo.id, sender="user", text=text))
        db.session.commit()

        # 3️⃣ Build context (limit last 10 messages)
        messages = (
            Message.query.filter_by(conversation_id=convo.id)
            .order_by(Message.id.desc())
            .limit(10)
            .all()[::-1]
        )
        context = build_context(messages)

        # 4️⃣ AI call
        ai_result = analyze_symptoms(text, context, agent_type)

        # 5️⃣ Save bot reply
        db.session.add(
            Message(conversation_id=convo.id, sender="bot", text=ai_result["reply"])
        )
        db.session.commit()

        return jsonify(
            {
                "status": "success",
                "reply": ai_result["reply"],
                "confidence_score": ai_result["confidence_score"],
                "conversation_id": convo.id,
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
