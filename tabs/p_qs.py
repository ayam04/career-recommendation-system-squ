import streamlit as st
from utils import *


def show_p_qs():
    try:
        if 'questions2' not in st.session_state:
            st.session_state.questions2 = get_p_questions()

        questions2 = st.session_state.questions2 if 'questions2' in st.session_state else []

        temporary_answers_dict2 = {}

        if 'answers_dict2' not in st.session_state:
            st.session_state.answers_dict2 = {question: "" for question in questions2}

        st.header("Personality Based Questions")
        for idx, question in enumerate(questions2):
            answer = st.text_input(question, key=f"temp_dict2_{idx}")
            temporary_answers_dict2[question] = answer

        if st.button('Submit', key="submit_p_qs"):
            for question in questions2:
                st.session_state.answers_dict2[question] = temporary_answers_dict2.get(question, "")
            st.success("Your answers have been saved. Please proceed to the next section.")
            st.write(st.session_state.answers_dict2)
    except Exception as e:
        st.exception(e)

show_p_qs()