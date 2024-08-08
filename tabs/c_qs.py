import streamlit as st
from utils import *

def show_c_qs():
    try:
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        if st.session_state.user_data["edu"] == "in School right now":
            if 'questions1' not in st.session_state:
                st.session_state.questions1 = get_i_questions()
        elif st.session_state.user_data["edu"] == "in University right now":
            if 'questions1' not in st.session_state:
                st.session_state.questions1 = get_g_questions()

        questions1 = st.session_state.questions1 if 'questions1' in st.session_state else []

        if 'answers_dict1' not in st.session_state:
            st.session_state.answers_dict1 = {question: "" for question in questions1}
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0

        st.header("Career Based Questions:")
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if st.session_state.current_question < len(questions1):
            current_question = questions1[st.session_state.current_question]

            if not any(m["content"] == current_question for m in st.session_state.chat_messages):
                with st.chat_message("assistant"):
                    st.markdown(current_question)
                st.session_state.chat_messages.append({"role": "assistant", "content": current_question})

            if answer := st.chat_input("Your answer:", key=f"chat_input_{st.session_state.current_question}"):
                st.session_state.chat_messages.append({"role": "user", "content": answer})
                st.session_state.answers_dict1[current_question] = answer
                
                st.session_state.current_question += 1
                st.rerun()

        if st.session_state.current_question >= len(questions1):
            st.success("Thank you for answering all the questions! You can generate your Career Report now. ")
            # st.write("Here are your answers:")
            # st.write(st.session_state.answers_dict1)
            # st.success("Your answers have been saved. Please proceed to the next section.")

    except Exception as e:
        # print(e)
        st.error("Please complete the questions in User data.")

show_c_qs()