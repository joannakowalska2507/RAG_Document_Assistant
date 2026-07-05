from rag.llm import llm
def generate_title(question: str):
    prompt = f"""
    Zadanie: Na podstawie poniższego pytania stwórz krótki tytuł rozmowy.

    Wymagania:
    - język: polski
    - max 6 słów
    - bez znaków interpunkcyjnych
    - styl naturalny (jak nazwa notatki)Na podstawie poniższego pytania stwórz krótki tytuł rozmowy.
   

    Pytanie: {question}
    """

    return llm.invoke(prompt).content.strip()