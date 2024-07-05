import streamlit as st
import re

def get_name():
    name = st.text_input("Enter your name:")
    return name
        

def get_age():
    age = st.number_input("Enter your age:", step=1, min_value=1, max_value=100)
    return age

def get_email():
    email = st.text_input("Enter your email:")
    return email

def get_edu():
    options = ["in School right now", "in University right now"]
    edu = st.radio("Select your educational qualification:", options)
    return edu

def get_interest():
    interest = st.text_input("Do you have any specific interests:")
    return interest

def get_grades():
    grade = st.file_uploader("Upload your grades here in a PDF or Excel sheet:", type=["pdf", "xlsx", "xls", "csv"])
    return grade

def is_valid_email(email):
  email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*\.\w{2,}$"
  return re.match(email_regex, email) is not None

def entry_check(data):
    count = 0
    for i in data.keys():
        if data[i] == "" or data[i] == None:
            break
        else:
            count += 1
    return count


def show_user_data():
    st.title("Career Recommendation System")
    st.write("This system will help you find the best career path for you based on your interests and personality.")
    st.header("Please enter your details below:")

    col1, col2 = st.columns(2)

    with col1:
        name = get_name()
        age = get_age()
        edu = get_edu()
    
    with col2:
        email = get_email()
        interest = get_interest()
        grades = get_grades()
    
    if st.button("Submit"):

        data = {
            "name": name,
            "age": age,
            "email": email,
            "edu": edu,
            "interest": interest,
            "grades": grades
        }

        if entry_check(data)==6:
            if is_valid_email(data["email"]):
                st.session_state.user_data = data
                st.write(st.session_state.user_data)
                st.success("Your details have been saved. Please proceed to the next section.")
            else:
                st.error("Please enter a valid email address.")
        else:
            st.error("Please fill all the fields before submitting.")