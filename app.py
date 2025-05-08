
import streamlit as st
import fitz  # PyMuPDF
import openai

# Set your OpenAI API key here
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your-api-key-here"

st.title("AI CV Reviewer")
st.write("Upload your CV as a PDF or paste it below for instant AI feedback.")

# File uploader
uploaded_file = st.file_uploader("Upload your CV (PDF format)", type=["pdf"])

# Text area fallback
cv_text = ""
if uploaded_file is not None:
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        cv_text = text
        st.success("PDF uploaded and text extracted successfully.")
    except Exception as e:
        st.error("Error reading PDF: " + str(e))
else:
    cv_text = st.text_area("Or paste your CV text here:", height=300)

if st.button("Review My CV"):
    if not cv_text.strip():
        st.warning("Please upload a PDF or paste your CV text.")
    else:
        with st.spinner("Analyzing your CV with AI..."):
            try:
                prompt = f"Please review the following CV and give detailed, professional feedback for improvement:

{cv_text}"
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800
                )
                feedback = response['choices'][0]['message']['content']
                st.subheader("AI Feedback:")
                st.write(feedback)
            except Exception as e:
                st.error("An error occurred: " + str(e))
