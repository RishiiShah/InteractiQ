# Author: MrSentinel

import streamlit as st
import google.generativeai as palm
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("PALM_API_KEY")
palm.configure(api_key=API_KEY)

def main():
    st.set_page_config(page_title="Chat with PaLM", page_icon="🤖")

    st.image("stream.jpg", use_column_width=False, width=400)
    st.title("Chat with InteractiQ")
    st.write("Welcome! Chat with us, a language model.")
    prompt = st.text_input("Enter your prompt here:", help="Type your prompt here...")

    temp = st.slider("Temperature", 0.0, 1.0, 0.75, step=0.05, help="Temperature controls the randomness of the generated text.")

    if st.button("Send", help="Generate response based on the prompt"):

        model = "models/text-bison-001"
        response = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=temp,
            max_output_tokens=1024
        )
        st.header("Response:")
        st.markdown(response.result, unsafe_allow_html=False)


main()
