import streamlit as st
import requests

# Page settings
st.set_page_config(page_title="Prana AI", layout="centered")

# App title
st.title("Prana AI Chatbot Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask your health question...")

# When user sends message
if user_input:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to backend
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={
            "message": user_input,
            "history": st.session_state.messages
        }
    )

    data = response.json()

    ai_response = data.get(
        "response",
        "Error getting AI response"
    )

    # Store AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)