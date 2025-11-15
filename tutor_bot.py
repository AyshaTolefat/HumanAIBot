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

prompt = st.chat_input(
    "Enter a topic and/or attach an image",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "pdf"],
)

if "messages" not in st.session_state:
    st.session_state.messages =[{"role":"assistant","content":"Please upload your document so we can get started!"}]

if st.sidebar.button("New Chat"):
    st.session_state.messages =[{"role":"assistant","content":"Please upload your document so we can get started!"}]
    #st.session_state.messages =[]
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"].text)
        else:
            st.markdown(message["content"])
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt.text)

if st.button("View Results"):
    st.switch_page("pages/results.py")

