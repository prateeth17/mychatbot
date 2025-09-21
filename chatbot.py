import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)
if "messages" not in st.session_state.keys():  # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",   # you can also use "gemini-1.5-pro"
    google_api_key=st.secrets["GOOGLE_API_KEY"]  # Fixed key name
)
conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

# Streamlit UI
st.title("🗣️ Conversational Chatbot")
st.subheader("💡 Powered by Google Gemini")

if prompt := st.chat_input("Your question"):  # Prompt for user input
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input=prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)