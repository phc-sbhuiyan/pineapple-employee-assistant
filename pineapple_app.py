import streamlit as st
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
import time

IsRunning = False

def setup_pineapple_branding_and_text():
    st.set_page_config(page_title='Staypineapple Employee Assistant', page_icon = 'https://www.staypineapple.com/skins/skin-pineapple-hospitality/favicon.ico', layout="wide")
    st.logo(
        "https://www.staypineapple.com/skins/skin-pineapple-hospitality/assets/desktop/images/logo.svg",
        icon_image="https://lh3.googleusercontent.com/o1lnTsMUxZZKJZ56s2wd7x2up7VZRmGf6V6zdzyeC9r7-_Quq0jo--vJOSIMTHLSWJA=s256-c",
    )
    st.sidebar.markdown("Welcome to 🍍 Staypineapple Employee Assistant!")

    #for right side logo
    logo_url = "https://www.staypineapple.com/skins/skin-pineapple-hospitality/assets/desktop/images/logo.svg"
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h1>Welcome Pineapples!</h1>
            <img src="{logo_url}" style="height: 50px;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    #hiding footer by streamlit
    hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def initialize_pinecone():
        api_key = st.secrets["PINECONE_API_KEY"]
        pc = Pinecone(api_key=api_key)
        assistant = pc.assistant.Assistant(
            assistant_name="pineapple-employee-assistant-bot", 
        )
        return assistant

def initialize_openai():
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    return client

def retrieve_answer(assistant, query, json_mode):
    if query:
        with st.chat_message("user"):
                st.markdown(user_query)
        IsRunning = True
        msg = Message(role="user", content=query)
        resp = assistant.chat(messages=[msg])
        IsRunning = False
        
        st.write(answer.content)
        st.markdown(answer)
        st.session_state.messages.append(resp.message)
        return resp.message
    else:
        st.warning("Please enter a query.")

def main(assistant):
    #audio_value = st.audio_input("record a voice message to transcribe")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "Hello Pineapple, please click to record or type your query."}]

    client = initialize_openai()
    audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=41_000)
    transcript_text = '';
    if audio_bytes:
         audio_location = "audio_file.wav"
         with open(audio_location, "wb") as f:
                f.write(audio_bytes)

         with open(audio_location, "rb") as fa:
                transcript = client.audio.transcriptions.create(model="whisper-1", file = fa)
                transcript_text = transcript.text
         st.write(transcript_text)
         user_query = transcript_text

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User query input
    user_query = st.text_input("Enter your query:")
    if st.button("Submit", on_click=retrieve_answer, args=(assistant, user_query, "")):
        progress_text = "Operation in progress, Please wait..."
        progressBar = st.progress(0, text=progress_text)
        percent_complete = 0
        while True:
            time.sleep(0.5)
            progressBar.progress(percent_complete + 1, text=progress_text)
            percent_complete += 1
            if IsRunning == True:
                break
        time.sleep(0.5)
        progressBar.empty()
        user_query = '';

setup_pineapple_branding_and_text()

if __name__ == "__main__":
    pa = initialize_pinecone()
    #st.sidebar.markdown("# :blue[Options]")
    #full_response = st.sidebar.expander("Full response", expanded=False)
    main(pa)
