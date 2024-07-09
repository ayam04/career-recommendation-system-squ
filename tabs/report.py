import streamlit as st
from functions import get_report

def show_report():
    try:
        user_data = st.session_state.user_data
        c_qs_ans = st.session_state.answers_dict1
        p_qs_ans = st.session_state.answers_dict2

        st.header("Your Career Report:")

        if st.button('Generate Report', key="generate_report"):
            with st.spinner("Generating your report..."):
                report = get_report(user_data, c_qs_ans, p_qs_ans)
                st.write(report)
    except Exception as e:
        print(e)
        st.error("Please complete all the assessment questions.")