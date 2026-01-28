from flask import Blueprint, request, jsonify
from Chatbot.models import db, Conversation, Message
from Chatbot.services.ai_engine import analyze_symptoms
from Chatbot.services.context_manager import build_context

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)

        user_id = str(data.get("user_id", "")).strip()
        text = str(data.get("message", "")).strip()

        if not user_id or not text:
            return jsonify({"status": "error", "message": "user_id and message required"}), 400

        convo = Conversation.query.filter_by(user_id=user_id).first()
        if not convo:
            convo = Conversation(user_id=user_id)
            db.session.add(convo)
            db.session.commit()

        user_msg = Message(
            conversation_id=convo.id,
            sender="user",
            text=text
        )
        db.session.add(user_msg)
        db.session.commit()

        messages = Message.query.filter_by(conversation_id=convo.id).all()
        context = build_context(messages)

        reply = analyze_symptoms(text, context)

        bot_msg = Message(
            conversation_id=convo.id,
            sender="bot",
            text=reply
        )
        db.session.add(bot_msg)
        db.session.commit()

        return jsonify({
            "status": "success",
            "reply": reply,
            "conversation_id": convo.id
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
