import os
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Check whether API key exists
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found. "
        "Please add your OpenAI API key to the .env file."
    )


# PDF location
# "." means the current project folder
PDF_DIRECTORY = "."


# Text chunk settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# Number of documents to retrieve
RETRIEVAL_K = 4


# OpenAI embedding model
EMBEDDING_MODEL = "text-embedding-3-small"


# OpenAI chat model
LLM_MODEL = "gpt-4.1-mini"