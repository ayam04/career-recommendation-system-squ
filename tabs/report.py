import streamlit as st
from functions import get_report
from utils import get_images, get_job_listings
import json

# col1, col2 = st.columns(2)

def show_report():
    try:
        user_data = st.session_state.user_data
        c_qs_ans = st.session_state.answers_dict1
        p_qs_ans = st.session_state.answers_dict2

        # col1, col2 = st.columns(2)
        st.header("Your Career Report:")

        if st.button('Generate Report', key="generate_report"):
            try:
                with st.spinner("Generating Your Report!"):
                    report = json.loads(get_report(user_data, c_qs_ans, p_qs_ans))
                    image_url_1, image_url_2 = get_images(report.get("word", ""))
                    job1 , job2 = get_job_listings(report.get("word", "")) 
                    st.write(report["para1"])
                    st.write(report["para2"])
                    with st.spinner("Loading image.."):
                        st.image(image_url_1, use_column_width=True)
                    st.write(report["para3"])
                    with st.spinner("Loading image.."):
                        st.image(image_url_2, use_column_width=True)
                    st.write(report["para4"])
                    st.header("Some Job Listings for you:")
                    st.link_button("Job 1", job1, type="secondary")
                    st.link_button("Job 2", job2, type="secondary")
            except Exception as e:
                print(e)
                st.error(f"An error occurred while generating the report: {e}")

    except Exception as e:
        print(e)
        st.error(f"Please complete all the assessment questions: {e}")