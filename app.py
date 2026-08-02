import os
import streamlit as st
import pandas as pd

from dbop import (
    ts_result,
    tp_result,
    p_result,
    ls_result,
    get_products,
    search_products
)

from chatbot import get_ai_response


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Database Assistant",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# CSS
# -----------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# -----------------------------
# Chat Function
# -----------------------------
def render_chat(db_path):

    st.subheader("💬 AI Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask anything about your database...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("🤖 Thinking..."):

            response = get_ai_response(
                prompt,
                db_path
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        with st.chat_message("assistant"):
            st.write(response)


# ===========================================================
# Sidebar
# ===========================================================

st.sidebar.title("⚙ Database Source")

database_mode = st.sidebar.radio(
    "Choose Database",
    [
        "🏪 Supermarket",
        "📂 Upload Custom Database"
    ]
)


# ===========================================================
# SUPERMARKET MODE
# ===========================================================

if database_mode == "🏪 Supermarket":

    db_path = "Supermarket.db"

    st.markdown(
        """
        <div class="ai-header">
            🤖 Supermarket AI Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", ts_result)
    col2.metric("Profit", p_result)
    col3.metric("Products", tp_result)
    col4.metric("Low Stock", ls_result)

    st.subheader("Inventory")

    product_search = st.text_input("SEARCH PRODUCT")

    if product_search.strip() == "":
        products = get_products()
    else:
        products = search_products(product_search)

    df = pd.DataFrame(
        products,
        columns=[
            "Product",
            "Stock",
            "Cost",
            "Selling"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    render_chat(db_path)


# ===========================================================
# CUSTOM DATABASE MODE
# ===========================================================

else:

    st.title("🤖 AI Database Assistant")

    st.write(
        "Upload any SQLite database (.db) and ask questions in natural language."
    )

    uploaded_file = st.sidebar.file_uploader(
        "Upload SQLite Database",
        type=["db", "sqlite", "sqlite3"]
    )

    if uploaded_file is None:

        st.info("Upload a database from the sidebar to begin.")

        st.stop()

    os.makedirs("uploaded_databases", exist_ok=True)

    db_path = os.path.join(
        "uploaded_databases",
        uploaded_file.name
    )

    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Database Loaded: {uploaded_file.name}")

    st.write(f"**Current Database:** `{uploaded_file.name}`")

    render_chat(db_path)