import streamlit as st
import PyPDF2
from langchain_mistralai import ChatMistralAI
import ast
import json

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

if "topic_list" not in st.session_state:
    st.session_state.topic_list = []

if "generate_topic" not in st.session_state:
    st.session_state.generate_topic = True

if "topic_one_q" not in st.session_state:
    st.session_state.topic_one_q = False

if "topic_two_q" not in st.session_state:
    st.session_state.topic_two_q = False

if "topic_three_q" not in st.session_state:
    st.session_state.topic_three_q = False

if "topic_four_q" not in st.session_state:
    st.session_state.topic_four_q = False

if "topic_five_q" not in st.session_state:
    st.session_state.topic_five_q = False

if "finish" not in st.session_state:
    st.session_state.finish = False

if "topic_one_answers" not in st.session_state:
    st.session_state.topic_one_answers = ["","","",""]

if "topic_two_answers" not in st.session_state:
    st.session_state.topic_two_answers = ["","","",""]

if "topic_three_answers" not in st.session_state:
    st.session_state.topic_three_answers = ["","","",""]

if "topic_four_answers" not in st.session_state:
    st.session_state.topic_four_answers = ["","","",""]

if "topic_five_answers" not in st.session_state:
    st.session_state.topic_five_answers = ["","","",""]

if "topic_one_correct" not in st.session_state:
    st.session_state.topic_one_correct = ""

if "topic_two_correct" not in st.session_state:
    st.session_state.topic_two_correct = ""

if "topic_three_correct" not in st.session_state:
    st.session_state.topic_three_correct = ""

if "topic_four_correct" not in st.session_state:
    st.session_state.topic_four_correct = ""

if "topic_five_correct" not in st.session_state:
    st.session_state.topic_five_correct = ""

if  "topic_one_questions" not in st.session_state:
    st.session_state.topic_one_questions = ""

if  "topic_two_questions" not in st.session_state:
    st.session_state.topic_two_questions = ""

if  "topic_three_questions" not in st.session_state:
    st.session_state.topic_three_questions = ""

if  "topic_four_questions" not in st.session_state:
    st.session_state.topic_four_questions = ""

if  "topic_five_questions" not in st.session_state:
    st.session_state.topic_five_questions = ""

if "topic_one_generated" not in st.session_state:
    st.session_state.topic_one_generated = False

if "topic_two_generated" not in st.session_state:
    st.session_state.topic_two_generated = False

if "topic_three_generated" not in st.session_state:
    st.session_state.topic_three_generated = False

if "topic_four_generated" not in st.session_state:
    st.session_state.topic_four_generated = False

if "topic_five_generated" not in st.session_state:
    st.session_state.topic_five_generated = False

if "topic_one_score" not in st.session_state:
    st.session_state.topic_one_score = False

if "topic_two_score" not in st.session_state:
    st.session_state.topic_two_score = False

if "topic_three_score" not in st.session_state:
    st.session_state.topic_three_score = False

if "topic_four_score" not in st.session_state:
    st.session_state.topic_four_score = False

if "topic_five_score" not in st.session_state:
    st.session_state.topic_five_score = False

if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "topic_one_score_analysis" not in st.session_state:
    st.session_state.topic_one_score_analysis = ""

if "topic_two_score_analysis" not in st.session_state:
    st.session_state.topic_two_score_analysis = ""

if "topic_three_score_analysis" not in st.session_state:
    st.session_state.topic_three_score_analysis = ""

if "topic_four_score_analysis" not in st.session_state:
    st.session_state.topic_four_score_analysis = ""

if "topic_five_score_analysis" not in st.session_state:
    st.session_state.topic_five_score_analysis = ""


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

def summarize_material(material: str, user_text: str = "") -> str:
    """Return a short summary and instruction to generate topics."""
    llm = get_llm()
    prompt = f"""
You are a concise study assisstant.
The student has provided the following study material and possibly a short message.

STUDY MATERIAL:
--------------
{material[:4000]}
--------------

STUDENT MESSAGE:
{user_text}

TASK: 
1. Write a brief summary of the main ideas in the study material in at most 3-4 sentences.
2. The summary MUST be a single short paragraph.
3. Then, on a new line, tell the stduent exactly this:
Press the 'Generate Topics' button to identify key topics, then press each topic button to answer quiz questions for each topic."
RULES:
-Do NOT write more than one short paragraph of summary.
-Do NOT add any other instructions or commentary.
"""
    response = llm.invoke(prompt)
    return response.content

def identify_topics(num_topics: int=5) -> str:
    material = st.session_state.get("source_text", "").strip()
    if not material:
        return (
            "I dont have any material yet."
            "Please type a topic or upload a PDF."
        )
    llm = get_llm()
    prompt = f"""
You are a helpful tutor. Your task if to identify the five key topics in the study material provided.

STUDY MATERIAL:{material[:6000]}

You should output the topics in this format: "Topic 1","Topic 2","Topic 3","Topic 4","Topic 5"
Don't include any other text only the ouput in the format.

"""

    response = llm.invoke(prompt)

    topic_list = response.content

    topic_list = [x.strip().strip('"') for x in topic_list.split(",")]

    st.session_state.topic_list = topic_list

    topic_list_text = ", ".join(topic_list)

    topic_message = (
        f"I have identified the key topics: {topic_list_text}.\n\n"
        "I am going to ask you questions on each topic. "
        "Press the topic button to move on to the next topic."
    )

    return topic_message

def generate_questions(topic_name,num_questions: int=4):
    material = st.session_state.get("source_text", "").strip()
    if not material:
        return (
            [],
            "I dont have any material yet."
            "Please type a topic or upload a PDF."
        )
    llm = get_llm()
    prompt = f"""
You are a helpful tutor. Your task is to create questions based on the pdf provided by the student to test the student's understanding based ONLY on the study material provided. The goal is to find the student's weak points and strengths in the material they provided you with.

You should create four multiple choice questions based on the provided topic using only the material provided.

STUDY MATERIAL:
--------------
{material[:6000]}
--------------
TASK: 
-Create EXACTLY {num_questions} multiple-choice questions.
- Each question MUST be directly answerable from the study material.
-Each question MUST have 4 options.

RESPONSE FORMAT:
Respond with ONLY valid JSON. No explanations. No extra text.
The JSON must be a list of objects like this:
[
    {{
        "question": "What is ...?",
        "options": [
            "first option text",
            "second option text",
            "third option text",
            "fourth option text",
        ]
    }},
    ...
]

RULES:
-Do NOT incldue the correct answers in the JSON.
-Do NOT label options with A/B/C/D in the text. Just the option text.
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    try:
        start = raw.find("[")
        end = raw.rfind("]")
        if start != -1 and end != -1:
            json_str = raw[start : end + 1]
        else:
            json_str = raw

        questions = json.loads(json_str)
        if not isinstance(questions, list) or not questions:
            return [], "Quiz generation failed: response was not a non-empty list."

        md_lines = [f"**{topic_name}**", ""]
        letters = ["A", "B", "C", "D"]
        for idx, q in enumerate(questions):
            md_lines.append(f"**Q{idx+1}. {q.get('question', '')}**")
            opts = q.get("options", [])
            for j, opt in enumerate(opts[:4]):
                md_lines.append(f"{letters[j]}) {opt}")
            md_lines.append("")  # blank line between questions

        markdown_text = "\n".join(md_lines)
        return questions, markdown_text

    except Exception as e:
        return [], f"Quiz generation failed while parsing JSON: {e}\nRaw response:\n{raw}"




def generate_score(answers,correct):
    score = 0

    correct = correct.strip("[]")
    correct = [x.strip().strip('"').strip("'") for x in correct.split(",")]

    for i in range(len(answers)):
        if answers[i] == correct[i]:
            score+=1
    
    percentage = (score/4)*100

    return percentage

def score_analysis(answers, correct):
    right = []
    wrong = []

    correct = correct.strip("[]")
    correct = [x.strip().strip('"').strip("'") for x in correct.split(",")]

    for i in range(len(answers)):
        if answers[i] == correct[i]:
            right.append(i + 1)
        else:
            wrong.append(i + 1)

    output = ""
    if right:
        output += "You got Questions " + ", ".join(map(str, right)) + " right. "
    else:
        output += "You got no questions right. "
    
    if wrong:
        output += "You got Questions " + ", ".join(map(str, wrong)) + " wrong."
    else:
        output += "You got no questions wrong."

    return output

def analyse_topic_answers(answers, correct_str):
    """Return 2 lists: questions numbers that are right and wrong."""
    correct_str = correct_str.strip("[]")
    correct_list = [
        x.strip().strip('"').strip('"')
        for x in correct_str.split(",")
        if x.strip()
    ]
    right = []
    wrong = []
    for i, ans in enumerate(answers):
        if not ans:
            continue
        if i < len(correct_list) and ans == correct_list[i]:
            right.append(i+1)
        else:
            wrong.append(i+1)
    return right, wrong
    

def show_options(form_name,topic_index, question_objs, answers, correct_str):
    """
    Render each question with its options, and store chosen A/B/C/D letters in 'answers' ONLY after the user submits. Then show which questions were correct/incorrect.
    """
    letters = ["A", "B", "C", "D"]
 
    with st.form(form_name):
        st.markdown(f"### Questions for topic {topic_index + 1}")

        temp_choices = []

        for i, q in enumerate(question_objs):
            st.markdown(f"**Question {i+1}. {q.get('question', '')}**")

            opts = q.get("options", [])
            opts = (opts + ["", "", "", ""])[:4]
            labeled_options = ["Select an answer..."] + [f"{letters[j]}) {opts[j]}" for j in range(4)]
            exisiting = answers[i] if i < len(answers) else ""
            if exisiting in letters:
                default_index = letters.index(exisiting) + 1
            else:
                default_index= 0
            choice = st.radio(
                "Options",
                labeled_options,
                index=default_index,
                key=f"{form_name}_q{i}",
            )

            temp_choices.append(choice)
            st.markdown("---")
        submitted = st.form_submit_button("Submit")

    if submitted:
        for i, choice in enumerate(temp_choices):
            if choice.startswith("Select"):
                answers[i] = ""
            else:
                answers[i] = choice[0]
        right, wrong = analyse_topic_answers(answers, correct_str)
        if right:
            st.success("✅ Correct:" + ",".join(f"Q{n}" for n in right))
        if wrong:
            st.error("❌ Incorrect:" + ",".join(f"Q{n}" for n in wrong))
        if "" in answers:
            st.warning("Please answer all questions before moving to the next topic.")
        else:
            st.info("You have answered all questions for this topic. You may move onto the next topic.")
    
def generate_answers(questions):
    material = st.session_state.get("source_text", "").strip()
    if not material:
        return (
            "I dont have any material yet."
            "Please type a topic or upload a PDF."
        )
    llm = get_llm()
    prompt = f"""
You are a helpful tutor. Your task is to generate answers to provided questions based on only the material provided.
You will be provided with a list of multiple choice questions and you must return the answers.

STUDY MATERIAL:
--------------
{material[:6000]}

QUESTIONS: {questions}

You should output the answers in this format: ["A","B","C","D"] where entry one is the answer to question 1 etc. Only provide the answers not exta text.

"""
    response = llm.invoke(prompt)

    answer_list = response.content

    return answer_list

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
            if pdf_text and st.session_state.get("generate_topic", True):
                with st.spinner("Summarizing your document..."):
                    answer = summarize_material(pdf_text, user_text)
            else:
                with st.spinner("Thinking..."):
                    answer = ask_mistral(combined_text)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.get("source_text"):

    if st.session_state.generate_topic:
        if st.button("Generate Topics"):
            with st.chat_message("assistant"):
                with st.spinner("Generating topics from your material..."):
                    topic_list = identify_topics()
                st.markdown(topic_list)
            st.session_state.messages.append({"role": "assistant", "content": topic_list})
            st.session_state.topic_one_q = True
            st.session_state.generate_topic = False

def display_questions(topic_index,topic_flag,next_topic_flag,answers_key,button_label):

    if st.session_state.get(topic_flag, False):
        if st.button(button_label):
            with st.chat_message("assistant"):
                with st.spinner(f"Generating questions for Topic {topic_index+1}..."):
                    q_objs, q_markdown = generate_questions(
                        st.session_state.topic_list[topic_index]
                    )

                    if not q_objs:
                        st.markdown(q_markdown) 
                    else:
                        st.session_state[f"{answers_key}_question_objs"] = q_objs
                        st.session_state[f"{answers_key}_questions"] = q_markdown
                        st.session_state[f"{answers_key}_generated"] = True
                        st.session_state[f"{answers_key}_correct"] = generate_answers(
                            st.session_state[f"{answers_key}_questions"]
                        )

                        st.session_state.messages.append(
                            {"role": "assistant", "content": q_markdown}
                        )
        if st.session_state.get(f"{answers_key}_generated", False):
            q_objs = st.session_state.get(f"{answers_key}_question_objs", [])
            if q_objs:
                show_options(
                    form_name=answers_key,
                    topic_index=topic_index,
                    question_objs=q_objs,
                    answers=st.session_state[f"{answers_key}_answers"],
                    correct_str=st.session_state[f"{answers_key}_correct"]
                )
                if all(st.session_state[f"{answers_key}_answers"]):
                    st.session_state[next_topic_flag] = True

def get_topic_label(idx: int) -> str:
    topics = st.session_state.get("topic_list", [])
    if idx < len(topics):
        return topics[idx]
    return f"Topic {idx + 1}"

if st.session_state.topic_one_q:
    display_questions(topic_index=0,
    topic_flag="topic_one_q",
    next_topic_flag="topic_two_q",
    answers_key="topic_one",
    button_label=get_topic_label(0),)

if st.session_state.topic_two_q:
    display_questions(topic_index=1,
    topic_flag="topic_two_q",
    next_topic_flag="topic_three_q",
    answers_key="topic_two",
    button_label=get_topic_label(1),)

if st.session_state.topic_three_q:
    display_questions(topic_index=2,
    topic_flag="topic_three_q",
    next_topic_flag="topic_four_q",
    answers_key="topic_three",
    button_label=get_topic_label(2),)

if st.session_state.topic_four_q:
    display_questions(topic_index=3,
    topic_flag="topic_four_q",
    next_topic_flag="topic_five_q",
    answers_key="topic_four",
    button_label=get_topic_label(3),)

if st.session_state.topic_five_q:
    display_questions(topic_index=4,
    topic_flag="topic_five_q",
    next_topic_flag="finish",
    answers_key="topic_five",
    button_label=get_topic_label(4),)

if st.session_state.finish:
    st.session_state.show_results = True
    st.session_state.topic_one_score = generate_score(st.session_state.topic_one_answers,st.session_state.topic_one_correct)
    st.session_state.topic_two_score = generate_score(st.session_state.topic_two_answers,st.session_state.topic_two_correct)
    st.session_state.topic_three_score = generate_score(st.session_state.topic_three_answers,st.session_state.topic_three_correct)
    st.session_state.topic_four_score = generate_score(st.session_state.topic_four_answers,st.session_state.topic_four_correct)
    st.session_state.topic_five_score = generate_score(st.session_state.topic_five_answers,st.session_state.topic_five_correct)

    st.session_state.topic_one_score_analysis = score_analysis(st.session_state.topic_one_answers,st.session_state.topic_one_correct)
    st.session_state.topic_two_score_analysis = score_analysis(st.session_state.topic_two_answers,st.session_state.topic_two_correct)
    st.session_state.topic_three_score_analysis = score_analysis(st.session_state.topic_three_answers,st.session_state.topic_three_correct)
    st.session_state.topic_four_score_analysis = score_analysis(st.session_state.topic_four_answers,st.session_state.topic_four_correct)
    st.session_state.topic_five_score_analysis = score_analysis(st.session_state.topic_five_answers,st.session_state.topic_five_correct)

    if st.button("View Results"):
        st.switch_page("pages/results.py")
