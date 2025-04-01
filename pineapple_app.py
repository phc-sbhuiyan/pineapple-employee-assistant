import streamlit as st
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI

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
    msg = Message(role="user", content=query)

    resp = assistant.chat(messages=[msg])
    return resp.message

def main(assistant):
    #audio_value = st.audio_input("record a voice message to transcribe")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant"}]

    client = initialize_openai()
    audio_bytes = audio_recorder("Click to record", "Click to stop recording")
    transcript_text = '';
    if len(audio_bytes) > 0:
         st.audio(audio_bytes.export().read())
         audio.export("audio.wav", format="wav")
         with open("audio.wav", "rb") as audio_file:
                 transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file = audio_file
                )
         transcript_text = transcript.text
         st.write(transcript_text)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User query input
    user_query = transcript_text    #st.text_input("Enter your query:")
    if st.button("Submit"):
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)
            
            answer = retrieve_answer(assistant, user_query, "")
            st.write(answer.content)
            st.markdown(answer)
            st.session_state.messages.append(answer)
            full_response.write(answer)
        else:
            st.warning("Please enter a query.")



if __name__ == "__main__":

    pa = initialize_pinecone()
    
    st.sidebar.markdown("# :blue[Options]")
    
    full_response = st.sidebar.expander("Full response", expanded=False)

    main(pa)
