from langchain_openai import ChatOpenAI

from config import (
    RETRIEVAL_K,
    LLM_MODEL
)

from prompts import SYSTEM_PROMPT

from ingest import build_knowledge_base


class KnowledgeBase:

    def __init__(self):

        print("\nCreating knowledge base...")

        # Build ChromaDB in memory
        self.vector_store = (
            build_knowledge_base()
        )

        # Create retriever
        self.retriever = (
            self.vector_store.as_retriever(
                search_kwargs={
                    "k": RETRIEVAL_K
                }
            )
        )

        # Create OpenAI LLM
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0
        )

        print(
            "Knowledge base initialized successfully."
        )


    def retrieve_documents(self, question):
        """
        Retrieve relevant document chunks.
        """

        documents = self.retriever.invoke(
            question
        )

        return documents


    def create_context(self, documents):
        """
        Convert retrieved documents into
        context for the LLM.
        """

        context_parts = []

        for index, document in enumerate(
            documents
        ):

            source_file = document.metadata.get(
                "source_file",
                "Unknown"
            )

            page = document.metadata.get(
                "page",
                "Unknown"
            )

            # PyPDFLoader uses zero-based page numbers
            if isinstance(page, int):

                page = page + 1

            context = f"""
SOURCE {index + 1}

Document: {source_file}
Page: {page}

Content:
{document.page_content}
"""

            context_parts.append(
                context
            )

        return "\n".join(
            context_parts
        )


    def ask(self, question):
        """
        Ask a question and return:
        - answer
        - source documents
        """

        # Retrieve relevant chunks
        documents = self.retrieve_documents(
            question
        )

        # Create context
        context = self.create_context(
            documents
        )

        # Create system prompt
        system_message = SYSTEM_PROMPT.format(
            context=context
        )

        # Send question to LLM
        messages = [
            (
                "system",
                system_message
            ),
            (
                "human",
                question
            )
        ]

        response = self.llm.invoke(
            messages
        )

        answer = response.content

        return answer, documents