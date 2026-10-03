import streamlit as st

from rag import KnowledgeBase


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Knowledge Base",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# APPLICATION TITLE
# ==========================================

st.title("📚 AI-Powered Knowledge Base")

st.write(
    "Ask questions about your uploaded PDF documents "
    "and get grounded answers with source citations."
)


# ==========================================
# LOAD KNOWLEDGE BASE
# ==========================================

@st.cache_resource
def load_knowledge_base():

    return KnowledgeBase()


try:

    knowledge_base = (
        load_knowledge_base()
    )

except Exception as error:

    st.error(
        f"Failed to initialize knowledge base: {error}"
    )

    st.stop()


# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==========================================
# CHAT INPUT
# ==========================================

question = st.chat_input(
    "Ask a question about your PDFs..."
)


if question:

    # ------------------------------
    # Display user question
    # ------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # ------------------------------
    # Generate answer
    # ------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents..."
        ):

            try:

                answer, documents = (
                    knowledge_base.ask(
                        question
                    )
                )

                # Display answer
                st.markdown(answer)


                # --------------------------
                # Source citations
                # --------------------------

                st.markdown(
                    "### 📚 Sources"
                )

                displayed_sources = set()

                for document in documents:

                    source_file = (
                        document.metadata.get(
                            "source_file",
                            "Unknown"
                        )
                    )

                    page = (
                        document.metadata.get(
                            "page",
                            "Unknown"
                        )
                    )

                    if isinstance(page, int):

                        page = page + 1


                    source = (
                        source_file,
                        page
                    )


                    # Avoid duplicate sources
                    if source not in displayed_sources:

                        displayed_sources.add(
                            source
                        )

                        st.markdown(
                            f"- 📄 **{source_file}** "
                            f"— Page **{page}**"
                        )


            except Exception as error:

                st.error(
                    f"An error occurred: {error}"
                )