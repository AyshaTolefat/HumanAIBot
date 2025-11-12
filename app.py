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

st.sidebar.title("Chat history")

prompt = st.chat_input(
    "Enter a topic and/or attach an image",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "pdf"],
)
