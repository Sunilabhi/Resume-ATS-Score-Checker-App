import streamlit as st
import os
import PyPDF2 as pdf
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

# Function to get AI response
def get_response(query):
    response = model.generate_content(query)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Input prompt for the generative AI
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and provide the best assistance for improving resumes.
Assign a percentage match based on JD and identify missing keywords with high accuracy.
resume:{text}
description:{Job_Description}

I want the response in a single string with the structure:
{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}
"""

# Streamlit App Interface

# App Title and description
st.set_page_config(page_title="Resume ATS Evaluator", page_icon="📄")
st.title("🚀 Resume ATS Checker")
st.write("**Optimize your resume for better job applications in tech!**\n"
         "Upload your resume and provide a job description to find out how well you match the role.")

# Job Description input field
st.subheader("📋 Job Description")
Job_Description = st.text_area("Enter the job description you are applying for", height=150)

# Upload PDF resume
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type="pdf", help="Please upload a PDF version of your resume.")

# Submit button
submit = st.button("📝 Analyze Resume")

# Analyze the resume upon submission
if submit:
    if uploaded_file and Job_Description:
        with st.spinner('Analyzing your resume...'):
            # Extract text from uploaded PDF
            text = input_pdf_text(uploaded_file)


            # Prepare the input prompt for the AI model
            #query = input_prompt.format(text=resume_text, jd=Job_Description)

            # Get the response from AI
            response = get_response(input_prompt)
            #st.write(text)

            # Display results in a neat format
            try:
                result = json.loads(response)  # Parse response to a dictionary
                st.success(f"🎯 **JD Match**: {result['JD Match']}")
                st.write(f"📝 **Profile Summary**: {result['Profile Summary']}")
                if result['MissingKeywords']:
                    st.warning("🔑 **Missing Keywords**:")
                    st.write(', '.join(result['MissingKeywords']))
                else:
                    st.success("✅ **No Missing Keywords** found!")
            except json.JSONDecodeError:
                st.error("Failed to analyze the resume. Please try again.")
    else:
        st.warning("Please upload a resume and enter a job description to proceed.")

# Footer with branding or additional information
st.markdown("""
---
*Powered by Streamlit & Google Generative AI*  
*Developed by Sunilkumar (#)*
""")



