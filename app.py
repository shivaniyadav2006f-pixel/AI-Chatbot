import streamlit as st
from datetime import datetime
from file_processor import process_file
import requests
from config import UNSPLASH_ACCESS_KEY
from streamlit_mic_recorder import mic_recorder
from voice import speak
from image_search import search_image
from web_search import web_search
from chatbot import chat
from database import save_message, load_messages, clear_messages


# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)


# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = load_messages()


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:

    st.title("🤖 AI Chatbot")

    st.markdown("---")


    model = st.selectbox(
        "Choose AI Model",
        [
            "llama3.2:latest",
            "phi3:mini"
        ]
    )


    st.markdown("---")


    uploaded_file = st.file_uploader(
        "📂 Upload File",
        type=[
            "pdf",
            "docx",
            "txt",
            "xlsx",
            "pptx"
        ]
    )


    if uploaded_file is not None:

        st.success(
            f"✅ {uploaded_file.name} uploaded successfully"
        )


        with st.spinner("📖 Reading file..."):
            file_text = process_file(uploaded_file)

        st.session_state["document"] = file_text

        # Show first 1000 characters of the document
        st.write("### PDF Text Preview")
        st.write(file_text[:1000])

        st.success("📄 File Ready ✅")
    st.markdown("---")


    if st.button("🗑 Clear Chat"):

        clear_messages()
        st.session_state.messages = []

        st.rerun()

    st.markdown("---")


    st.subheader("📊 Chat Statistics")


    user_messages = len(
        [
            m for m in st.session_state.messages
            if m["role"] == "user"
        ]
    )


    ai_messages = len(
        [
            m for m in st.session_state.messages
            if m["role"] == "assistant"
        ]
    )


    st.write(
        f"👤 Questions : {user_messages}"
    )

    st.write(
        f"🤖 Responses : {ai_messages}"
    )


    st.markdown("---")


    st.write(
        "🕒",
        datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )
    )



    st.markdown("---")


    st.info(
"""
### About

🤖 AI Chatbot

✅ Streamlit

✅ Ollama

✅ Chat History

✅ File Upload

✅ Multiple AI Models
"""
    )



# ----------------------------
# Main Title
# ----------------------------

st.title(
    "🤖 AI Chatbot using Ollama"
)

st.caption(
    "Powered by Streamlit + Ollama"
)



# ----------------------------
# Chat History
# ----------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



# ----------------------------
# Chat Input
# ----------------------------
audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder",
    use_container_width=True,
)

prompt = st.chat_input(
    "Ask me anything..."
)

if prompt:

    # ----------------------------
    # Image Search
    # ----------------------------

    image_words = [
        "image",
        "photo",
        "picture",
        "show me"
    ]

    if any(word in prompt.lower() for word in image_words):

        query = prompt.lower()

        for word in image_words:
            query = query.replace(word, "")

        query = query.strip()

        image_url = search_image(query)

        if image_url:

            with st.chat_message("assistant"):
                st.image(image_url, caption=query)

            st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    save_message("user", prompt)

    with st.chat_message("user"):

        st.markdown(prompt)



    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            try:
                # ----------------------------
                # Web Search
                # ----------------------------

                web_keywords = [
                    "latest",
                    "today",
                    "news",
                    "weather",
                    "current",
                    "live"
                ]

                if any(word in prompt.lower() for word in web_keywords):
                    web_result = None

                    if web_result:

                        st.session_state.messages.append(
                            {
                                "role": "system",
                                "content": f"Use this latest web information:\n\n{web_result}"
                            }
                        )
                if "document" in st.session_state:
                    system_message = {
                        "role": "system",
                        "content": f"""
You are a helpful AI assistant.

The following is the complete content of the uploaded document.

---------------- DOCUMENT START ----------------

{st.session_state["document"]}

---------------- DOCUMENT END ----------------

Instructions:

- Use the uploaded document as your primary source.
- If the answer exists in the document, answer using the document.
- If the answer is not found in the document, answer using your own knowledge.
- Do not say that no document was uploaded.
- Do not ask the user to upload the document again because it is already provided above.
"""
                    }
                    messages = [system_message] + st.session_state.messages
                else:
                    messages = st.session_state.messages

                # 🌐 Web Search for latest/current information
                web_keywords = [
                    "latest",
                    "today",
                    "news",
                    "weather",
                    "current",
                    "live"
                ]

                if any(word in prompt.lower() for word in web_keywords):

                    web_data = web_search(prompt)
                    st.write(web_data)

                    system_message = {
                        "role": "system",
                        "content": f"""
Use the following latest web search results while answering.

{web_data}
"""
                    }

                    messages = [system_message] + messages

                answer = chat(
    model,
    messages
)
                st.markdown(answer)

                # 🔊 Voice Output
                audio_path = speak(answer)

                audio_file = open(audio_path, "rb")
                st.audio(audio_file.read(), format="audio/mp3")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )
                save_message("assistant", answer)
            except Exception as e:
                st.error(
                    f"❌ Error: {e}"
                )



# ----------------------------
# Download Chat
# ----------------------------

chat_history = ""


for message in st.session_state.messages:

    chat_history += (

        f"{message['role'].upper()}:\n"

        f"{message['content']}\n\n"

    )



st.sidebar.download_button(

    label="📥 Download Chat",

    data=chat_history,

    file_name="chat_history.txt",

    mime="text/plain"

)
