from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import  RunnableLambda
from rag.vector_store import vectorstore
from rag.llm import llm

retriever = vectorstore.as_retriever(search_kwargs={"k":3})
def format_docs(doc):
    return "\n\n".join(d.page_content for d in doc)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Odpowiedz używając  kontekstu oraz  historii,odpowiadaj krótko , ZAWSZE nie wiecej niz 4 zdania, używając języka w którym jest pytanie "),
    ("user", """
Historia:
{history}

Kontekst:
{context}

Pytanie:
{question}
""")
])

format_docs=RunnableLambda(format_docs)

rag_chain=(
    {
        "context": RunnableLambda(lambda x: x["question"]) | retriever | format_docs,
        "question": RunnableLambda(lambda x: x["question"]),
        "history": RunnableLambda(lambda x: x["history"]),
    }
    |prompt
    |llm
    |StrOutputParser()
)

def rag_ask(question: str, history: str = ""):
    return rag_chain.invoke({
        "question": question,
        "history": history
    })
