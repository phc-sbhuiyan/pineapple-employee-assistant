import streamlit as st
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

def initialize_pinecone():
        api_key = st.secrets["PINECONE_API_KEY"]
        pc = Pinecone(api_key=api_key)
        assistant = pc.assistant.Assistant(
            assistant_name="pineapple-employee-assistant-bot", 
        )
        return assistant

def retrieve_answer(assistant, query, json_mode):
    msg = Message(role="user", content=query)

    resp = assistant.chat(messages=[msg],
                          json_response=json_mode
                          )
    return resp.message

def main(assistant):
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant"}]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User query input
    user_query = st.text_input("Enter your query:")
    if st.button("Submit"):
        if user_query:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            answer = retrieve_answer(assistant, user_query, json_mode)
            if json_mode:
                st.json(answer.content)
            else:
                st.write(answer.content)
            st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            full_response.write(answer)
        else:
            st.warning("Please enter a query.")



if __name__ == "__main__":
    
    pa = initialize_pinecone()
    st.sidebar.markdown("# :blue[Options]")
    full_response = st.sidebar.expander("Full response", expanded=False)

    main(pa)
