"""
Creates policy retriever.
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

#------------Ingestion--------------
loader=TextLoader("data/travel_policy.md")

documents=loader.load()

# Recursive chunking
splitter=RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=20) 

chunks=splitter.split_documents(documents)

embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store=FAISS.from_documents(chunks,embeddings)

retriever=vector_store.as_retriever(search_kwargs={"k":3})

print("Vector store created successfully")

#-------------Retriever----------------
def retrieve_policy(query):
    docs=retriever.invoke(query)

    result= "\n\n".join(doc.page_content for doc in docs)

    return result