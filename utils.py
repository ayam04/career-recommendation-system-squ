import json
import random

def get_p_questions():
    with open('Questions\p-questions.json', 'r') as file:
        questions = json.load(file)
    random_questions = random.sample(questions, 10)
    questions_answers_dict = {question: "" for question in random_questions}
    return questions_answers_dict

def get_i_questions():
    with open('Questions\i-questions.json', 'r') as file:
        questions = json.load(file)
    random_questions = random.sample(questions, 10)
    questions_answers_dict = {question: "" for question in random_questions}
    return questions_answers_dict

def get_g_questions():
    with open('Questions\g-questions.json', 'r') as file:
        questions = json.load(file)
    random_questions = random.sample(questions, 10)
    questions_answers_dict = {question: "" for question in random_questions}
    return questions_answers_dict

print(get_p_questions())
print(get_i_questions())
print(get_g_questions())
