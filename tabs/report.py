import streamlit as st
from functions import get_report
from utils import get_images, get_job_listings, send_email, get_job_listings_google, read_template
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
                    job3, job4= get_job_listings_google(report.get("word",""))

                    # Prepare the email body by passing the report and job links
                    email_body = f"""
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Career Report</title>
                        <style>
                            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap');

                            body {{
                                background-color: black;
                                color: #ffffff;
                                font-family: sans-serif;
                                text-align: justify;
                                margin: 0;
                            }}
                            .container {{
                                background-color: rgba(70, 69, 69, 0.75);
                                padding: 20px;
                                border-radius: 15px;
                                max-width: 800px;
                                margin: 30px auto;
                                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
                            }}
                            a {{
                                color: #ffcc00;
                                text-decoration: none;
                                font-weight: 500;
                                transition: color 0.3s ease;
                            }}
                            a:hover {{
                                color: #ffaa00;
                            }}
                            p {{
                                line-height: 1.7;
                                font-size: 17px;
                            }}
                            h2 {{
                                color: #ffdd57;
                                text-align: center;
                                margin-bottom: 20px;
                            }}
                            .image {{
                                display: block;
                                margin: 20px auto;
                                max-width: 100%;
                                border-radius: 12px;
                            }}
                            ul {{
                                padding-left: 20px;
                                margin: 20px 0;
                            }}
                            li {{
                                margin-bottom: 10px;
                            }}
                            .footer {{
                                margin-top: 40px;
                                text-align: center;
                                font-size: 15px;
                                color: #cccccc;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h2>CareerSage Report</h2>

                            <p>{report["para1"]}</p>
                            <p>{report["para2"]}</p>
                            <img src="cid:image1" class="image" alt="Career Image 1"/>

                            <p>{report["para3"]}</p>
                            <p>{report["para4"]}</p>
                            <img src="cid:image2" class="image" alt="Career Image 2"/>

                            <h2>Job Listings:</h2>
                            <ul>
                                <li><a href="{job1}">Job 1</a></li>
                                <li><a href="{job2}">Job 2</a></li>
                                <li><a href="{job3}">Job 3</a></li>
                                <li><a href="{job4}">Job 4</a></li>
                            </ul>

                            <p class="footer">Best regards,<br>CareerSage</p>
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
                    col1, col2 = st.columns(2)
                    with col1:
                        st.link_button("Job 1", job1, type="secondary")
                        st.link_button("Job 2", job2, type="secondary")
                    with col2:
                        st.link_button("Job 3", job3, type="secondary")
                        st.link_button("Job 4", job4, type="secondary")

            except Exception as e:
                st.error(f"An error occurred while generating the report: {e}")
                print(f"Error: {e}")

    except Exception as e:
        print(e)
        st.error(f"Please complete all the assessment questions.")
