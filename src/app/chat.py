import streamlit as st

from src.services.server import server


class Chat:

    def __init__(self):
        self.server = server

    def chat_box(self):
        messages = st.container(height=500)

        # Initialize Chat History
        if "messages" not in st.session_state:
            st.session_state.messages = [
                dict(role="assistant", content=f"Hello {st.session_state.user}! How can I help you today?")]

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            messages.chat_message(message["role"]).write(message["content"])

        if prompt := st.chat_input("Say something"):
            messages.chat_message("user").write(prompt)
            user_message = dict(role="user", content=prompt)
            st.session_state.messages.append(user_message)
            bot_response = self.server.send_message_to_chatbot(user=st.session_state.user, message=prompt)
            if bot_response:
                messages.chat_message("assistant").write(bot_response)
                bot_message = dict(role="assistant", content=bot_response)
                st.session_state.messages.append(bot_message)
