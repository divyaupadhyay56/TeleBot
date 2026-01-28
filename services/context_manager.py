def build_context(messages):
    context = ""
    for msg in messages[-5:]:  # last 5 messages
        context += f"{msg.sender}: {msg.text}\n"
    return context
