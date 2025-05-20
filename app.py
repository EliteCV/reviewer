import streamlit as st
import openai
import fitz  # PyMuPDF
import os
# --- This must be the first Streamlit command ---
st.set_page_config(page_title="EliteCV - AI CV Reviewer", layout="centered")
# --- Title and instructions ---
st.title("EliteCV - AI CV Reviewer")
st.markdown("Upload your CV as a PDF or paste it below for instant AI feedback.")
# --- Email input at the top ---
email = st.text_input("Enter your email (optional)", placeholder="you@example.com")

# Optional: Save email to file
if email:
    with open("emails.txt", "a") as f:
        f.write(email + "\n")
# --- File uploader ---
uploaded_file = st.file_uploader("Upload your CV (PDF format)", type=["pdf"])

if uploaded_file is not None:
    # Extract text from PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    st.success("PDF uploaded and text extracted successfully.")

    if st.button("Review My CV"):
        with st.spinner("Analyzing your CV..."):
            openai.api_key = os.getenv("OPENAI_API_KEY")
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful career coach who gives clear, specific CV feedback."},
                        {"role": "user", "content": f"Please review my CV and suggest improvements:\n\n{text}"}
                    ],
                    temperature=0.7
                )
                feedback = response.choices[0].message.content
                st.markdown("### AI Feedback:")
                st.write(feedback)
            except Exception as e:
                st.error(f"Something went wrong: {e}") 
