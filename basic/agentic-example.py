import asyncio
import uuid
from dotenv import load_dotenv
import streamlit as st
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_default_openai_client,
    set_tracing_disabled,
)
from openai.types.responses import ResponseTextDeltaEvent 
import os 

load_dotenv()
api_key = os.getenv("OLLAMA_API_KEY")
base_url = os.getenv("OLLAMA_ENDPOINT")
set_tracing_disabled(True)


custom_client = AsyncOpenAI(base_url=base_url, api_key=api_key)
set_default_openai_client(custom_client)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful reasoning assistant",
    model=OpenAIChatCompletionsModel(        model="llama3.2",
        openai_client=custom_client,
    ), 
)

st.set_page_config(
    page_title="AI  Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e6f7ff;
        border-left: 5px solid #2196F3;
    }
    .chat-message.assistant {
        background-color: #f0f0f0;
        border-left: 5px solid #4CAF50;
    }
    .chat-message .content {
        display: flex;
        margin-top: 0.5rem;
    }
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .message {
        flex: 1;
        color: #000000;
    }
    .timestamp {
        font-size: 0.8rem;
        color: #888;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history and user context
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


if "processing_message" not in st.session_state:
    st.session_state.processing_message = None

st.title("AI Assistant")
st.write("Enter your question this will respond in real-time.")
user_input = st.text_area("Your question:", "")

async def stream_response(prompt):
    # Create a placeholder for the streaming output
    response_placeholder = st.empty()
    full_response = ""


    result = Runner.run_streamed(agent, prompt)
    # Use stream_events() instead of stream
    async for event in result.stream_events():
        # Handle raw response events for text streaming
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
             # Append new text to the full response
            full_response += event.data.delta
            # Update the placeholder with the accumulated text
            response_placeholder.markdown(full_response)
            print(event.data.delta, end="", flush=True)

# Handle the submit button
if st.button("Submit") and user_input:
    # Create a spinner while waiting for the response
    with st.spinner("Thinking..."):
        # Run the async function in a way that works with Streamlit
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(stream_response(user_input))
        finally:
            loop.close()

# Sidebar for user preferences
with st.sidebar:
    st.title("Travel Preferences")
    
    st.subheader("About You")


#if __name__ == "__main__":
    # Run the async function in the event loop
   # asyncio.run(stream_response())
