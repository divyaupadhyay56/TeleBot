from flask import Blueprint, request, jsonify
from TeleBot.models import db, Message

sync_bp = Blueprint("sync", __name__)

@sync_bp.route("/sync", methods=["GET"])
def sync_get():
    messages = Message.query.order_by(Message.id.desc()).all()

    result = []
    for m in messages:
        result.append({
            "id": m.id,
            "conversation_id": m.conversation_id,
            "sender": m.sender,
            "text": m.text,
            "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({
        "status": "success",
        "messages": result
    })


@sync_bp.route("/sync", methods=["POST"])
def sync_post():
    data = request.get_json(force=True)

    msg = Message(
        text=data.get("message"),
        sender="user",
        conversation_id=1
    )

    db.session.add(msg)
    db.session.commit()

    return jsonify({"status": "saved", "id": msg.id})
