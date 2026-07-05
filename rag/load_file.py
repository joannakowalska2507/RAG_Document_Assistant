from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader

def load_file(filepath):
    if filepath.endswith(".pdf"):
        loader = PyPDFLoader(filepath)
    elif filepath.endswith(".docx"):
        loader = Docx2txtLoader(filepath)
    elif filepath.endswith(".txt"):
        loader = TextLoader(filepath, encoding="utf-8")
    else:
        raise ValueError("Nieobsługiwany format pliku")

    return loader.load()