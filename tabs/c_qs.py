import streamlit as st
from utils import *


def show_c_qs():
    try:
        if 'questions1' not in st.session_state:
            st.session_state.questions1 = get_i_questions()

        questions1 = st.session_state.questions1 if 'questions1' in st.session_state else []

        temporary_answers_dict1 = {}

        if 'answers_dict1' not in st.session_state:
            st.session_state.answers_dict1 = {question: "" for question in questions1}
        st.header("Career Based Questions")
        for question in questions1:
            answer = st.text_input(question, key=f"temp_dict1_{question}")
            temporary_answers_dict1[question] = answer

        if st.button('Submit', key="submit_c_qs"):
            for question in questions1:
                st.session_state.answers_dict1[question] = temporary_answers_dict1.get(question, "")
            st.success("Your answers have been saved. Please proceed to the next section.")

    except Exception as e:
        st.exception(e)