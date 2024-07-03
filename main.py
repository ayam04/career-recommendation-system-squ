import streamlit as st
from utils import *
import json

questions1 = [
    "How do you identify your gender?",
    "What age are you, and how does it influence your perspective?",
    "Which country do you hail from, and what do you cherish most about it?",
    "What major are you passionate about in your Intermediate studies?",
    "Can you describe your overall experience in your Intermediate studies?"
]

questions2 = [
    "Which courses have you enjoyed the most and why?",
    "Have you completed your degree? If so, what are your future plans?",
    "Do you find joy in coding and programming?",
    "How do you feel about mathematics?",
    "What excites you about Physics?"
]

if 'answers_dict1' not in st.session_state:
    st.session_state.answers_dict1 = {question: "" for question in questions1}

if 'answers_dict2' not in st.session_state:
    st.session_state.answers_dict2 = {question: "" for question in questions2}

st.title("Questionnaire")

st.header("Section 1")
for question in questions1:
    answer = st.text_input(question, key=f"dict1_{question}")
    st.session_state.answers_dict1[question] = answer

st.header("Section 2")
for question in questions2:
    answer = st.text_input(question, key=f"dict2_{question}")
    st.session_state.answers_dict2[question] = answer

if st.button('Submit'):
    st.write("Here are your answers for Section 1:")
    st.write(json.dumps(st.session_state.answers_dict1, indent=4))

    st.write("Here are your answers for Section 2:")
    st.write(json.dumps(st.session_state.answers_dict2, indent=4))
