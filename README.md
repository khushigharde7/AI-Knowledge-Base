# 📚 AI-Powered Knowledge Base

An AI-powered Retrieval-Augmented Generation (RAG)
application that allows users to ask questions about
PDF documents and receive grounded answers with
source citations.

## Technologies

- Python
- OpenAI API
- LangChain
- ChromaDB
- PyPDF
- Streamlit

## Features

- Multiple PDF document support
- Automatic PDF text extraction
- Text chunking
- OpenAI embeddings
- ChromaDB vector search
- Retrieval-Augmented Generation
- Grounded responses
- Source citations
- Streamlit chat interface

## Setup

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a `.env` file:

OPENAI_API_KEY=your_api_key

Place PDF files directly in the project folder.

Run the application:

streamlit run app.py

## Example Questions

What is this document about?

What are the main findings?

Explain the methodology used in the research.

What problem does this document address?

What are the key conclusions?
