import streamlit as st
import requests
import json
from utils import check_ollama_installation, install_ollama, start_ollama_server, check_model_availability, pull_model, generate_response

def main():
    st.title("Illegal llama")
    
    # Check Ollama installation
    if not check_ollama_installation():
        st.error("Ollama is not running. Please install and start Ollama first.")
        if st.button("Install Ollama"):
            if install_ollama():
                if start_ollama_server():
                    st.success("Ollama installed and started successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to start Ollama server.")
            else:
                st.error("Failed to install Ollama.")
        return

    models = ["llama3.2", "dolphin-phi:2.7b", "llama2-uncensored:7b"]
    for model in models:
        available = check_model_availability(model_name=model)
        if not available: 
        	pull_model(model_name=model)

    # Sidebar for model selection and system prompt
    with st.sidebar:
        st.header("Settings")
        selected_model = st.selectbox("Choose a model:", models)
        system_prompt = st.text_area(
            "System prompt:",
            value="You are a helpful AI assistant.",
            height=100
        )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, selected_model, system_prompt)
                if response:
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Failed to generate response")

    # Clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

if __name__ == "__main__":
    main() 