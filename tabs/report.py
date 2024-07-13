import streamlit as st
from functions import get_report
from utils import get_images
import time

def show_report():
    try:
        user_data = st.session_state.user_data
        c_qs_ans = st.session_state.answers_dict1
        p_qs_ans = st.session_state.answers_dict2

        st.header("Your Career Report:")
        col1, col2 = st.columns(2)

        if st.button('Generate Report', key="generate_report"):
            try:
                with st.spinner("Generating Your Report!"):
                    start_time = time.time()
                    
                    report = get_report(user_data, c_qs_ans, p_qs_ans)
                    st.write(report)
                    # st.success(f"Report generated in {time.time() - start_time:.2f} seconds")

                    # start_time = time.time()
                    # image_url_1, image_url_2 = get_images(report["word"])
                    # st.success(f"Images fetched in {time.time() - start_time:.2f} seconds")

                    # st.write(report["para1"])
                    # st.write(report["para2"])
                    # with col1:
                    #     st.image(image_url_1, use_column_width=True)
                    # st.write(report["para3"])
                    # with col2:
                    #     st.image(image_url_2, use_column_width=True)
                    # st.write(report["para4"])

            except Exception as e:
                st.error(f"An error occurred while generating the report: {e}")

    except Exception as e:
        st.error(f"Please complete all the assessment questions: {e}")

show_report()
