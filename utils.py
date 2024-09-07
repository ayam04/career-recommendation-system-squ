import os
import re
import json
import random
import requests
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage  # Add this import
# from dotenv import load_dotenv

# load_dotenv()

# pix_api_key = os.getenv("PIX_API_KEY")
# adz_app_key = os.getenv("ADZ_APP_KEY")
# adz_api_key = os.getenv("ADZ_API_KEY")
pix_api_key = st.secrets["PIX_API_KEY"]
adz_app_key = st.secrets["ADZ_APP_KEY"]
adz_api_key = st.secrets["ADZ_API_KEY"]

picked_p_questions = set()
picked_i_questions = set()
picked_g_questions = set()

def get_p_questions():
    global picked_p_questions
    with open('Questions/p-questions.json', 'r') as file:
        questions = json.load(file)
    
    available_questions = {q: a for q, a in questions.items() if q not in picked_p_questions}
    
    if len(available_questions) < 10:
        print("Not enough new questions available.")
        return None
    
    random_questions = dict(random.sample(list(available_questions.items()), 10))
    picked_p_questions.update(random_questions.keys())
    
    return random_questions

def get_i_questions():
    global picked_i_questions
    with open('Questions/i-questions.json', 'r') as file:
        questions = json.load(file)
    
    available_questions = [q for q in questions if q not in picked_i_questions]
    if len(available_questions) < 6:
        print("Not enough new questions available.")
        return None
    
    random_questions = random.sample(available_questions, 6)
    picked_i_questions.update(random_questions)
    
    return random_questions

def get_g_questions():
    global picked_g_questions
    with open('Questions/g-questions.json', 'r') as file:
        questions = json.load(file)
    
    available_questions = [q for q in questions if q not in picked_g_questions]
    if len(available_questions) < 6:
        print("Not enough new questions available.")
        return None
    
    random_questions = random.sample(available_questions, 6)
    picked_g_questions.update(random_questions)
    
    return random_questions

def get_images(query):
    base_url = "https://pixabay.com/api/"
    params = {
        "key": pix_api_key,
        "q": query,
        "image_type": "photo",
        "lang": "en",
        "orientation": "horizontal",
    }
    try:
        response = requests.get(base_url, params=params)
        # print(response.url)
        response.raise_for_status()
        data = response.json()
        hits = len(data["hits"])
        if data["totalHits"] > 0:
            image_url_1 = data["hits"][random.randint(0,hits-1)]["largeImageURL"]
            image_url_2 = data["hits"][random.randint(0,hits-1)]["largeImageURL"]
            return (image_url_1, image_url_2)
        else:
            print("No images found")
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

def clean_response(response_text):
    json_objects = re.findall(r'\{.*?\}', response_text, re.DOTALL)
    print(json_objects)
    if len(json_objects) >= 2:
        cleaned_response = json_objects[:2]
        return cleaned_response
    else:
        print("Cleaning error")

def get_job_listings(query):
    endpoint = 'https://api.adzuna.com/v1/api/jobs/gb/search/1'
    params = {
        'app_id': adz_app_key,
        'app_key': adz_api_key,
        'results_per_page': 2,
        'what': query.strip(),
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        job1 = data["results"][0]['redirect_url']
        job2 = data["results"][1]['redirect_url']

        return (job1, job2)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

def send_email(recipient_email, subject, body, image_urls):
    sender_email = st.secrets["SENDER_EMAIL"]
    sender_password = st.secrets["SENDER_PASSWORD"]

    message = MIMEMultipart("related")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # HTML email body with updated CSS for colors
    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
                text-align: justify;
            }}
            .content {{
                margin: 20px;
            }}
            .image {{
                display: block;
                margin: 20px auto;
                max-width: 100%;
            }}
            a {{
                color: #1e90ff;  /* Change this to your desired link color */
                text-decoration: none;
            }}
            a:hover {{
                color: #ff4500;  /* Change the hover color if needed */
            }}
        </style>
    </head>
    <body>
        <div class="content">
            {body}
        </div>
    </body>
    </html>
    """

    message.attach(MIMEText(html_body, "html"))

    # Attach images
    for i, image_url in enumerate(image_urls):
        response = requests.get(image_url)
        img_data = response.content
        image = MIMEImage(img_data)
        image.add_header("Content-ID", f"<image{i+1}>")
        message.attach(image)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.set_debuglevel(1)  # Enable debug output for the SMTP connection
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"General Error: {e}")
        return False


# print(get_p_questions())
# print(get_i_questions())
# print(get_g_questions())
# print(get_images("psychology"))
# print(get_job_listings("Software engineering"))

