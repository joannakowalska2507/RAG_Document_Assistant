ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )
def format_history(messages):
    return "\n".join([
        f"{m['role']}: {m['content']}"
        for m in messages
    ])