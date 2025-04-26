import streamlit as st
import pandas as pd
import requests
import json
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App configuration
st.set_page_config(
    page_title="Interview Prep & Job Matching",
    page_icon="📝",
    layout="wide"
)

# Initialize session state
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = False
if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False
if "intake_complete" not in st.session_state:
    st.session_state.intake_complete = False

# Authentication placeholder (integrate OAuth later)
def authenticate():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Placeholder for actual authentication
        st.session_state.user_authenticated = True

# Main profile setup
def profile_setup():
    st.title("Set Up Your Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        zip_code = st.text_input("Zip Code")
        
    with col2:
        # Industry selection with multiselect
        industries = ["Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Retail"]
        selected_industries = st.multiselect("Industries of Interest", industries)
        
        # Salary expectations with slider
        salary_range = st.slider(
            "Salary Expectation Range (K USD)",
            min_value=30,
            max_value=200,
            value=(50, 80)
        )
    
    # Badges section
    st.subheader("Add Badges About Yourself")
    badge_col1, badge_col2, badge_col3 = st.columns(3)
    with badge_col1:
        personality_badges = st.multiselect(
            "Personality Type",
            ["INTJ", "INFJ", "INTP", "INFP", "ISTJ", "ISFJ", "ISTP", "ISFP", 
             "ENTJ", "ENFJ", "ENTP", "ENFP", "ESTJ", "ESFJ", "ESTP", "ESFP"]
        )
    with badge_col2:
        hobby_badges = st.multiselect(
            "Hobbies & Interests",
            ["Avid Reader", "Marathon Runner", "Yoga Enthusiast", "Coder", 
             "Musician", "Traveler", "Foodie", "Gamer"]
        )
    with badge_col3:
        skill_badges = st.multiselect(
            "Special Skills",
            ["Public Speaking", "Data Analysis", "Foreign Languages", 
             "Project Management", "Graphic Design", "Video Editing"]
        )
    
    # Save profile button
    if st.button("Save Profile"):
        # Placeholder for actual profile saving
        # In real implementation, would send this data to n8n webhook
        st.session_state.profile_complete = True
        st.success("Profile saved successfully!")

# Resume upload
def resume_upload():
    st.title("Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        # Save the file temporarily
        bytes_data = uploaded_file.getvalue()
        
        # Here you would send this to your n8n workflow
        # For MVP, just mark as uploaded
        st.session_state.resume_uploaded = True
        st.success("Resume uploaded successfully!")

# AI Intake simulation
def ai_intake():
    st.title("AI Intake Interview")
    
    # In a real implementation, this would be a websocket or API connection
    # to your OpenAI-powered chatbot via n8n
    
    st.write("Our AI will now ask you questions about your experience.")
    st.write("This helps us understand your background better than just a resume.")
    
    # Simulate chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! I'd like to learn more about your work experience. Could you tell me about your most recent role and what you did day-to-day?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("Your response")
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Simulate AI response
        # In actual implementation, this would call OpenAI via n8n
        with st.chat_message("assistant"):
            if len(st.session_state.messages) < 5:
                response = "Thanks for sharing! Next question: What were the main tools and technologies you used in this role?"
            elif len(st.session_state.messages) < 9:
                response = "Got it. Could you tell me about a challenging project you worked on and how you approached it?"
            else:
                response = "Thank you for completing the intake interview! We'll use this information to enhance your profile."
                st.session_state.intake_complete = True
            
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Practice interview function
def practice_interview():
    st.title("Practice Interview Questions")
    
    # Question categories
    categories = ["Behavioral", "Technical", "STAR Method", "Situational"]
    selected_category = st.selectbox("Select question type", categories)
    
    if selected_category == "Behavioral":
        question = "Tell me about a time you had to deal with a difficult team member."
    elif selected_category == "Technical":
        question = "Explain how you would approach implementing a database schema for this application."
    elif selected_category == "STAR Method":
        question = "Describe a situation where you had to meet a tight deadline. What was your task, what actions did you take, and what was the result?"
    else:
        question = "How would you handle a situation where your manager asks you to do something you disagree with?"
    
    st.subheader("Question:")
    st.write(question)
    
    answer = st.text_area("Your Answer", height=200)
    
    if st.button("Submit Answer"):
        if answer:
            # In real implementation, would send to OpenAI for feedback via n8n
            st.success("Answer submitted! Feedback coming soon.")
            
            # Placeholder feedback
            st.subheader("AI Feedback:")
            st.write("""
            Good start! Some suggestions:
            - Try using the STAR format more explicitly
            - Quantify your impact with specific metrics
            - Keep your answer more concise (aim for 2-3 minutes spoken)
            """)
        else:
            st.error("Please provide an answer before submitting.")

# Main app logic
def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    if not st.session_state.user_authenticated:
        authenticate()
    else:
        # Show progress in sidebar
        progress = 0
        if st.session_state.profile_complete:
            progress += 25
        if st.session_state.resume_uploaded:
            progress += 25
        if st.session_state.intake_complete:
            progress += 50
            
        st.sidebar.progress(progress/100)
        st.sidebar.write(f"Profile Completion: {progress}%")
        
        # Navigation options based on progress
        page = st.sidebar.radio(
            "Go to",
            ["Profile Setup", "Resume Upload", "AI Intake", "Practice Interview"]
        )
        
        if page == "Profile Setup":
            profile_setup()
        elif page == "Resume Upload":
            resume_upload()
        elif page == "AI Intake":
            if not st.session_state.resume_uploaded:
                st.warning("Please upload your resume first!")
            else:
                ai_intake()
        elif page == "Practice Interview":
            if not st.session_state.intake_complete:
                st.warning("Please complete the AI intake interview first!")
            else:
                practice_interview()

if __name__ == "__main__":
    main()