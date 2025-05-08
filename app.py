import streamlit as st
import openai

# Add your OpenAI API key here
openai.api_key = "sk-REPLACE-WITH-YOUR-API-KEY"

st.set_page_config(page_title="AI CV Reviewer", layout="centered")
st.title("AI CV Reviewer")
st.write("Paste your CV below and get AI-powered feedback in seconds.")

# Input area for CV
cv_input = st.text_area("Your CV", height=300, placeholder="Paste your CV here...")

# Button to trigger review
if st.button("Get AI Feedback"):
    if cv_input.strip() == "":
        st.warning("Please paste your CV first.")
    else:
        with st.spinner("Reviewing your CV..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a professional CV reviewer."},
                        {"role": "user", "content": f"Review this CV and give detailed improvement suggestions:\n\n{cv_input}"}
                    ],
                    temperature=0.7,
                    max_tokens=600
                )
                st.subheader("Feedback from AI")
                st.write(response.choices[0].message["content"])
            except Exception as e:
                st.error(f"Error: {e}")