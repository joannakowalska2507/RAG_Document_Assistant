from rag.load_file import load_file
from rag.splitter import split

def process_document(path):
    documents = load_file(path)
    chunks = split(documents)

    return chunks