import streamlit as st
import openai_secret_manager
import openai
from pdfminer.high_level import extract_text

with st.sidebar:
    secrets = openai_secret_manager.get_secret("openai")
    openai_api_key = secrets["api_key"]
    "View the source code"
    "!Open in GitHub Codespaces"

st.title("📝 File Q&A with OpenAI")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

if uploaded_file and question and openai_api_key:
    if uploaded_file.type == "application/pdf":
        article = extract_text(uploaded_file)
    else:
        article = uploaded_file.read().decode()
    prompt = f"Here's an article:\n\n<article>\n{article}\n\n</article>\n\n{question}\n"

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    answer = response["choices"][0]["text"]
    
    st.write("### Answer")
    st.write(answer)
