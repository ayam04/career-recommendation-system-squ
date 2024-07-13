import os
import re
import json
import random
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("PIX_API_KEY")

picked_p_questions = set()
picked_i_questions = set()
picked_g_questions = set()

def get_p_questions():
    global picked_p_questions
    with open('Questions/p-questions.json', 'r') as file:
        questions = json.load(file)
    
    available_questions = [q for q in questions if q not in picked_p_questions]
    if len(available_questions) < 10:
        print("Not enough new questions available.")
        return None
    
    random_questions = random.sample(available_questions, 10)
    picked_p_questions.update(random_questions)
    
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
        "key": api_key,
        "q": query,
        "image_type": "photo",
        "lang": "en",
        "orientation": "horizontal",
    }
    try:
        response = requests.get(base_url, params=params)
        print(response.url)
        response.raise_for_status()
        data = response.json()
        hits = len(data["hits"])
        if data["totalHits"] > 0:
            image_url_1 = data["hits"][random.randint(0,hits)]["largeImageURL"]
            image_url_2 = data["hits"][random.randint(0,hits)]["largeImageURL"]
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
    # print(json_objects)
    if len(json_objects) >= 2:
        cleaned_response = json_objects[:2]
        return cleaned_response
    else:
        print("Cleaning error")
    
# print(get_images("psychology"))
# print(get_p_questions())
# print(get_i_questions())
# print(get_g_questions())
