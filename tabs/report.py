import streamlit as st
from functions import get_report
from utils import get_images, get_job_listings, send_email
import json

def show_report():
    try:
        user_data = st.session_state.user_data
        c_qs_ans = st.session_state.answers_dict1
        p_qs_ans = st.session_state.answers_dict2

        st.header("Your Career Report:")

        if st.button('Generate Report', key="generate_report"):
            try:
                with st.spinner("Generating Your Report!"):
                    report = json.loads(get_report(user_data, c_qs_ans, p_qs_ans))
                    image_url_1, image_url_2 = get_images(report.get("word", ""))
                    job1, job2 = get_job_listings(report.get("word", ""))

                    # Prepare the email body with updated styling
                    email_body = f"""
                    <html>
                    <head>
                        <style>
                            body {{
                                background-color: black;
                                color: white;
                                font-family: Arial, sans-serif;
                                text-align: justify;
                                padding: 20px;
                            }}
                            a {{
                                color: #1e90ff;  /* Blue color for job links */
                                text-decoration: none;
                            }}
                            a:hover {{
                                color: #0044cc;  /* Darker blue on hover */
                            }}
                            .image {{
                                display: block;
                                margin: 20px auto;
                                max-width: 100%;
                            }}
                        </style>
                    </head>
                    <body>
                        <div>
                            <p>Dear {user_data['name']},</p>

                            <p>{report["para1"]}</p>

                            <p>{report["para2"]}</p>
                            <img src="cid:image1" class="image" />

                            <p>{report["para3"]}</p>

                            <p>{report["para4"]}</p>
                            <img src="cid:image2" class="image" />

                            <p>Job Listings:</p>
                            <ul>
                                <li><a href="{job1}">Job 1</a></li>
                                <li><a href="{job2}">Job 2</a></li>
                            </ul>

                            <p>Best regards,<br>Career Recommendation System</p>
                        </div>
                    </body>
                    </html>
                    """

                    # Send the email
                    if send_email(user_data["email"], "Your Career Report", email_body, [image_url_1, image_url_2]):
                        st.success(f"Your report has been sent to your email: {user_data['email']}")
                    else:
                        st.error("There was an error sending the email. Please check the logs for more details.")

                    # Display the report on the page
                    st.write(report["para1"])
                    st.write(report["para2"])
                    with st.spinner("Loading image.."):
                        st.image(image_url_1, use_column_width=True)
                    st.write(report["para3"])
                    with st.spinner("Loading image.."):
                        st.image(image_url_2, use_column_width=True)
                    st.write(report["para4"])
                    st.header("Some Job Listings for you:")
                    st.write(f"[Job 1]({job1})", unsafe_allow_html=True)
                    st.write(f"[Job 2]({job2})", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred while generating the report: {e}")
                print(f"Error: {e}")

    except Exception as e:
        print(e)
        st.error(f"Please complete all the assessment questions.")
