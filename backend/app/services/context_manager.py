def build_context(messages):
    context = []
    for msg in messages:
        context.append(f"{msg.sender}: {msg.text}")
    return "\n".join(context)
