from dotenv import load_dotenv
load_dotenv()
import os
import uuid
from werkzeug.utils import secure_filename
from file_service import save_file
from flask import Flask, render_template, request, jsonify, redirect
from rag.chat_chain import rag_ask
from db import *
from rag.vector_store import vectorstore
from utils import allowed_file,format_history
from rag.processor import process_document
from rag.title_generator import generate_title

app=Flask(__name__)

init_db()

UPLOAD_FOLDER = "docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/ask",methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question")
    conversation_id = data.get("conversation_id")
    if not question:
        return jsonify({"error": "Brak pytania"}), 400
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())
        title = generate_title(question)
        save_conversation(conversation_id, title)
    history = get_recent_messages(conversation_id, limit=4)
    history_text = format_history(history)
    answer = rag_ask(question,history_text)
    save_message(conversation_id, "użytkownik ", question)
    save_message(conversation_id, "asystent", answer)
    return jsonify({
        "answer": answer,
        "conversation_id": conversation_id
    })

@app.route("/upload")
def upload():
    return render_template("upload.html")
@app.route("/upload-file",methods=['POST'])
def upload_file():
    files = request.files.getlist("files")

    for file in files:
        if file.filename:
            if not allowed_file(file.filename):
                return {
                    "error": f" Pliki nie zostały dodane. \nPlik '{file.filename}' ma nieobsługiwany format."
                }, 400
            doc_id, path = save_file(file, UPLOAD_FOLDER)
            add_document(
                doc_id=doc_id,
                filename=secure_filename(file.filename),
                filepath=path
            )
            try:
                chunks = process_document(path)
                if not chunks:
                    delete_document(doc_id)
                    for f in os.listdir(UPLOAD_FOLDER):
                        if f.startswith(doc_id):
                            os.remove(os.path.join(UPLOAD_FOLDER, f))
                    raise ValueError(f"Błąd! Brak tekstu w pliku: {file.filename} \nPliki nie zostały dodane")

                for chunk in chunks:
                    chunk.metadata = {
                        "file_id": doc_id,
                        "filename": secure_filename(file.filename)
                    }
                vectorstore.add_documents(chunks)
            except ValueError as e:
                return {"error": str(e)}, 400


    return {"message": "Pliki zostały dodane ✔"}

@app.route("/view_docs")
def view_docs():
    files = get_documents()
    return render_template("view_docs.html", files=files)
@app.route("/delete/<doc_id>",methods=['POST'])
def delete_doc(doc_id):
    delete_document(doc_id)
    vectorstore.delete(where={"file_id": doc_id})
    for f in os.listdir(UPLOAD_FOLDER):
        if f.startswith(doc_id):
            os.remove(os.path.join(UPLOAD_FOLDER, f))
    return redirect("/view_docs")
@app.route("/history")
def history():
    conversations = get_all_conversations()
    return render_template("history.html",conversations=conversations)


@app.route("/delete_conv/<conv_id>",methods=['POST'])
def delete_conv(conv_id):
    delete_conversation(conv_id)
    return redirect("/history")
@app.route("/view_conv/<conv_id>")
def view_conv(conv_id):
    messages=get_conversation(conv_id)
    return render_template("view_conv.html",messages=messages)



@app.route("/description")
def descripton():
    return render_template("description.html")

if __name__ == "__main__":
    app.run(debug=True)