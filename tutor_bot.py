import streamlit as st
import PyPDF2
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

def get_llm():
    return ChatMistralAI(
        api_key=API_KEY,
        model="mistral-small-latest",
        temperature=0.3,
    )

def ask_mistral(user_text: str) -> str:
    llm = get_llm()
    response = llm.invoke(user_text)
    return response.content

def generate_quiz(num_questions: int=20) -> str:
    material = st.session_state.get("source_text", "").strip()
    if not material:
        return (
            "I dont have any material yet."
            "Please type a topic or upload a PDF."
        )
    llm = get_llm()
    prompt = f"""
You are a helpful tutor. Your task is to create a quiz based on the pdf provided by the student to test the student's understanding based ONLY on the study material provided. The goal is to find the student's weak points and strengths in the material they provided you with.

STUDY MATERIAL:
--------------
{material[:6000]}
--------------
TASK: 
-Create {num_questions} multiple-chocie questions.
- Each question should have four options: A, B, C, D.

FORMAT EXAMPLE:
Q1. What is ...?
A) ...
B) ...
C) ...
D) ...

Now generate the full quiz in this format.
"""
    response = llm.invoke(prompt)
    return response.content


def extract_text_from_pdfs(files):
    texts=[]
    for f in files:
        if f.type == "application/pdf":
            try:
                reader = PyPDF2.PdfReader(f)
                pdf_text = ""
                for page in reader.pages:
                    pdf_text += page.extract_text() or ""
                texts.append(pdf_text)
            except Exception as e:
                texts.append(f"[Error reading PDF {f.name}: {e}]")
    return "\n\n".join(texts)

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

    pdf_text = extract_text_from_pdfs(user_files)

    if "source_text" not in st.session_state:
        st.session_state.source_text = ""
    if pdf_text:
        st.session_state.source_text = pdf_text
    elif user_text:
        st.session_state.source_text = user_text

    if st.session_state.chat_title == "New chat" and user_text:
        st.session_state.chat_title = user_text

    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.markdown(user_text)
        for f in user_files:
            st.caption(f"Attached file: {f.name}")

    if pdf_text:
        combined_text = (
            "The student wants to study this material: \n\n"
            f"{pdf_text[:6000]}\n\n"
            "And they said:\n"
            f"{user_text}"
        )
    else:
        combined_text = user_text or ""

    with st.chat_message("assistant"):
        if not combined_text.strip():
            answer = "I didn't recieve any text or readable PDF content. Please type something or upload a PDF."
        else:
            with st.spinner("Thinking..."):
                answer = ask_mistral(combined_text)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.get("source_text"):
    if st.button("Generate quiz"):
        with st.chat_message("assistant"):
            with st.spinner("Generating quiz from your material..."):
                quiz_text = generate_quiz(num_questions = 20)
            st.markdown(quiz_text)
        st.session_state.messages.append({"role": "assistant", "content": quiz_text})

if st.button("View Results"):
    st.switch_page("pages/results.py")

