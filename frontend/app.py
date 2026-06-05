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
        "https://prana-ai-production.up.railway.app/chat",
        json={
            "message": user_input,
            "history": st.session_state.messages
        }
    )

    if response.status_code == 200:

        data = response.json()

        ai_response = data.get(
            "response",
            "Error getting AI response"
        )

else:

    ai_response = (
        f"Server Error: {response.status_code}"
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