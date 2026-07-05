import os
import uuid
from werkzeug.utils import secure_filename

def save_file(file, upload_dir):
    doc_id = str(uuid.uuid4())

    filename = secure_filename(file.filename)

    filename = f"{doc_id}_{filename}"
    path = os.path.join(upload_dir, filename)

    file.save(path)

    return doc_id, path
