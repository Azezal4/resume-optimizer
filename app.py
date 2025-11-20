import streamlit as st
import ollama
from docx import Document
from pypdf import PdfReader
import io

def extract_text_from_file(uploaded_file):
    """Extracts text from uploaded PDF or DOCX file."""
    text = ""
    file_type = uploaded_file.type
    
    # Handle PDF
    if "pdf" in file_type:
        try:
            reader = PdfReader(io.BytesIO(uploaded_file.read()))
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            return f"Error reading PDF: {e}"

    # Handle DOCX
    elif "document" in file_type or "docx" in file_type:
        try:
            document = Document(io.BytesIO(uploaded_file.read()))
            for paragraph in document.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            return f"Error reading DOCX: {e}"
            
    else:
        return "Unsupported file type. Please upload a PDF or DOCX file."
        
    return text

# --- 2. LLM Interaction Function ---
def get_modified_resume(resume_text, job_description, model="gemma3"):
    """Sends the resume and job description to Ollama for modification."""
    # Ollama Client is automatically configured to use the default host (http://localhost:11434)
    # If running in Docker Compose, the host must be set via the OLLAMA_HOST environment variable.
    client = ollama.Client()

    # The System Prompt is crucial for quality control
    system_prompt = (
        "You are an expert resume editor, dedicated to helping a candidate secure an interview. "
        "Your goal is to rewrite the provided resume to perfectly match the tone, required skills, "
        "and responsibilities listed in the job description. ONLY output the FULL, MODIFIED RESUME TEXT. "
        "Do not include any commentary, explanations, or headings like 'Modified Resume' or 'Here is the result'."
        "Do not add any symbols such as *, ** or *** while printing out the resume"
    )

    user_prompt = f"""
    JOB DESCRIPTION:
    ---
    {job_description}
    ---

    ORIGINAL RESUME TEXT:
    ---
    {resume_text}
    ---

    INSTRUCTION: Using the Job Description as your guide, rewrite the provided Original Resume Text to be maximally relevant. Focus on integrating keywords and quantifying achievements where possible. Output the complete, revised resume.
    """

    with st.spinner('Thinking... Gemma 3 is optimizing your resume. This may take a moment.'):
        try:
            response = client.chat(
                model=model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error communicating with Ollama (Gemma 3). Ensure the container is running and accessible. Error: {e}"


# --- 3. Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🤖 Gemma 3 Resume Optimizer (Local & Private)")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Resume & Job Description")

    # Resume Upload
    uploaded_file = st.file_uploader(
        "Upload your current Resume (PDF or DOCX)",
        type=["pdf", "docx"]
    )

    # Job Description Input
    job_description = st.text_area(
        "Paste the Job Description Here",
        height=300
    )

    run_button = st.button("🚀 Generate Optimized Resume", type="primary", use_container_width=True)

with col2:
    st.header("2. Optimized Resume Output")

    if run_button and uploaded_file and job_description:
        # Step A: Extract text from the resume file
        resume_text = extract_text_from_file(uploaded_file)

        if "Error" in resume_text:
            st.error(resume_text)
        else:
            # Step B: Call Gemma 3 to modify the resume
            modified_resume = get_modified_resume(resume_text, job_description, model="gemma3")

            # Step C: Display the result
            st.markdown("---")
            st.text_area(
                "Modified Resume",
                value=modified_resume,
                height=600,
            )
            st.download_button(
                "Download Modified Text",
                data=modified_resume,
                file_name="Optimized_Resume.txt",
                mime="text/plain"
            )

    elif run_button:
        st.warning("Please upload a resume and paste the job description to continue.")