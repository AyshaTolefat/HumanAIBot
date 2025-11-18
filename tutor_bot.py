import streamlit as st
from langchain_mistralai import ChatMistralAI
#from langchain.schema import HumanMessage, SystemMessage, AIMessage

st.title("Welcome to your own Tutor Bot!")
API_KEY= "4leOKUn3QNyLUB8sDAMw06kVXEqYJ1M7"
st.markdown(
    """
    This bot helps you understand your strengths and weaknesses in any topic you would like. 

    Start by giving a topic, or uploading a document to recieve some questions and identify your strengths and weaknesses.
    """
)

st.sidebar.title("Chat History")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New chat"

prompt = st.chat_input(
    "Enter a topic and/or attach an image",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "pdf"],
)

if "messages" not in st.session_state:
    st.session_state.messages =[{"role":"assistant","content":"Please upload your document so we can get started!"}]

for i, chat in enumerate(st.session_state.chat_history):
    if isinstance(chat, dict):
        raw_title = chat.get("title")
    else:
        raw_title = None

    if not isinstance(raw_title, str) or raw_title.strip() == "":
        raw_title = f"Chat {i+1}"

    if len(raw_title) > 25:
        raw_title = raw_title[:25] + "..."

    title = str(raw_title)

    if st.sidebar.button(title, key=f"history_{i}"):
        st.session_state.messages = chat["messages"]
        st.rerun()

if st.sidebar.button("New Chat"):
    has_user_message = any(m["role"] == "user" for m in st.session_state.messages)

    if has_user_message:
        title = st.session_state.get("chat_title") or f"Chat {len(st.session_state.chat_history) + 1}"

        st.session_state.chat_history.append(
            {
                "title": title,
                "messages": list(st.session_state.messages),
            }
        )
    st.session_state.messages =[{"role":"assistant","content":"Please upload your document so we can get started!"}]
    st.session_state.chat_title = "New chat"
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt is not None:
    user_text = prompt.text
    user_files = prompt.files

    if st.session_state.chat_title == "New chat" and user_text:
        st.session_state.chat_title = user_text

    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.markdown(user_text)
        for f in user_files:
            st.caption(f"Attached file: {f.name}")

if st.button("View Results"):
    st.switch_page("pages/results.py")

