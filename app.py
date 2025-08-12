import streamlit as st
import PyPDF2
import docx
import google.generativeai as genai

# Configure Gemini API
# Replace with your key
genai.configure(api_key="AIzaSyBkKFnyltZlmH-1ubY2IgFvJsGRCfR00Gc")

# Function to read PDF


def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to read DOCX


def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to optimise resume


def optimise_resume(resume_text, job_description):
    prompt = f"""
    You are an expert resume writer and ATS optimization specialist.
    Candidate's Resume:
    {resume_text}

    Target Job Description:
    {job_description}

    Task:
    1. Modify the resume to best match the job description.
    2. Keep formatting ATS-friendly (no tables/images).
    3. Add missing keywords naturally.
    4. Provide a brief summary of changes.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


# Streamlit UI
st.title("AI Resume Optimiser & Generator")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Target Job Description")

if uploaded_file and job_description:
    if uploaded_file.type == "application/pdf":
        resume_text = read_pdf(uploaded_file)
    else:
        resume_text = read_docx(uploaded_file)

    if st.button("Optimise Resume"):
        result = optimise_resume(resume_text, job_description)
        st.subheader("Optimised Resume & Changes")
        st.write(result)
