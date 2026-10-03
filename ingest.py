import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from config import (
    PDF_DIRECTORY,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL
)


def find_pdf_files():
    """
    Find all PDF files directly inside
    the project folder.
    """

    pdf_files = []

    for filename in os.listdir(PDF_DIRECTORY):

        if filename.lower().endswith(".pdf"):

            pdf_files.append(filename)

    return pdf_files


def load_pdf_documents():
    """
    Load all PDF documents.
    """

    pdf_files = find_pdf_files()

    if not pdf_files:

        raise FileNotFoundError(
            "No PDF files found in the project folder."
        )

    documents = []

    print("\nPDF files found:")

    for filename in pdf_files:

        print(f"  - {filename}")

        file_path = os.path.join(
            PDF_DIRECTORY,
            filename
        )

        loader = PyPDFLoader(file_path)

        pdf_documents = loader.load()

        # Add useful metadata
        for document in pdf_documents:

            document.metadata["source_file"] = filename

        documents.extend(pdf_documents)

    print(
        f"\nTotal pages loaded: {len(documents)}"
    )

    return documents


def split_documents(documents):
    """
    Split PDF text into smaller chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = text_splitter.split_documents(
        documents
    )

    print(
        f"Total chunks created: {len(chunks)}"
    )

    return chunks


def create_vector_store(chunks):
    """
    Create an in-memory ChromaDB vector store.
    """

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    print(
        "ChromaDB vector store created successfully."
    )

    return vector_store


def build_knowledge_base():
    """
    Complete ingestion pipeline.
    """

    print("\n==============================")
    print("AI KNOWLEDGE BASE INGESTION")
    print("==============================")

    documents = load_pdf_documents()

    chunks = split_documents(
        documents
    )

    vector_store = create_vector_store(
        chunks
    )

    print(
        "\nKnowledge base is ready!"
    )

    return vector_store


if __name__ == "__main__":

    build_knowledge_base()