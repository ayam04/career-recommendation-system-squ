import re
import warnings
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
# import os
# from utils import clean_response
# from dotenv import load_dotenv
# from langchain_community.llms.huggingface_hub import HuggingFaceHub

warnings.filterwarnings("ignore")

# load_dotenv()

# genai.configure(api_key=os.getenv("GEM_API_KEY"))
genai.configure(api_key=st.secrets["GEM_API_KEY"])

llm = genai.GenerativeModel("gemini-1.5-flash")

# os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_API_KEY")
# llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.1", model_kwargs={"temperature": 1, "max_new_tokens": 30000})

def get_report(user_data, c_qs_ans, p_qs_ans,):
    prompt = f"""You are a professional Career Counsellor. You majorly use the student's biodata, the students answers to some career based questions and the student's answers to some personality based questions to recommend a career path. You have been given the biodata of a student. The student is {user_data['name']}, {user_data['age']} years old, {user_data['edu']}, and has interests in {user_data['interest']}.
    The student has also uploaded a CV/Grade pdf having this test: {user_data["pdf_text"]}. The student answers to the career based questions are: {c_qs_ans}.
    The student's answers to the personality based questions are: {p_qs_ans}.
    
    Based on this information, recommend a career path for the student. Give some consideration to the user's interests too.
    
    You should follow a specific format for your response.
    
    Start with greeting the student first. Then thank the student for taking this test. Then based on the data provided, recommend a career path for the student. End with a closing note.
    
    You should avoid using any bold words or any special characters.
    You response should be at least 3 paragraphs of 5 to 6 lines each lines each that is close to 50 words each.
    Do not write anything before greetings.
    
    The first para should be 3 lines maximum.
    The second para and third para should be 5 to 6 lines maximum.
    
    Also follow this json format:

    {{"para1":"greetings to the user with their name \n content of the 1 para", "para2":"content of the 2 para","para3":"content of the 3 para","para4":"final closing statement to the user","word":"one word to describe the career path"}}

    Do not respond with anything other than the single line json.
    """
    # result = llm(prompt)
    result = llm.generate_content(prompt).text
    response = result.replace(prompt, "").strip().replace("\n\n", "\n").strip()
    response = re.sub(r'^.*?({.*?}).*$', r'\1', response)
    # with open("response.json", "w", encoding="utf-8") as file:
    #     file.write(response)
    # print(response)
    # response = clean_response(response)
    return response

def extract_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# extract_pdf_text("sample.pdf")
# get_report({"name": "Ayam", "age": 20, "edu": "in School right now", "interest": "playing football"}, {"are you good at football?":"yes"}, {"are you an extrovert?":"yes"})
