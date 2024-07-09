import re
import os
import warnings
from dotenv import load_dotenv
from langchain_community.llms.huggingface_hub import HuggingFaceHub

warnings.filterwarnings("ignore")

load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HF_API_KEY")

llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.2", model_kwargs={"temperature": 0.5, "max_new_tokens": 25000})

def get_report(user_data, c_qs_ans, p_qs_ans,):
    prompt = f"""You are a professional Career Counsellor. You majorly use the student's biodata, the students answers to some career based questions and the student's answers to some personality based questions to recommend a career path. You have been given the biodata of a student. The student is {user_data['name']}, {user_data['age']} years old, {user_data['edu']}, and has interests in {user_data['interest']}.
    The student has uploaded their grades. The student answers to the career based questions are: {c_qs_ans}.
    The student's answers to the personality based questions are: {p_qs_ans}.
    
    Based on this information, recommend a career path for the student. Give some consideration to the user's interests too.
    
    You should follow a specific format for your response.
    
    Start with greeting the student first. Then thank the student for taking this test. Then based on the data provided, recommend a career path for the student. End with a closing note.
    
    You should avoid using any bold words or any special characters.
    You response should be at least 3 paragraphs of 4 to 5 lines each.
    Do not write anything before greetings.
    """
    result = llm.generate([prompt])
    response = result.generations[0][0].text.replace(prompt, "").strip().replace("\n\n", "\n")
    print(response)
    return response

# get_report({"are you an extrovert?":"yes"}, {"are you good at football?":"yes"}, {"name": "John Doe", "age": 20, "edu": "in School right now", "interest": "playing football"})
