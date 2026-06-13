import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text

from chatbot import load_knowledge_base, find_best_answer
from database import init_db, save_conversation, get_conversations


st.set_page_config(
    page_title="AI Customer Support Chatbot & Voicebot",
    page_icon="🎙️",
    layout="wide",
)


def speak_answer_button(answer_text: str) -> None:
    """
    Browser-based text-to-speech.
    This avoids local audio package problems and works well for a demo.
    """
    safe_text = json.dumps(answer_text)

    components.html(
        f"""
        <button onclick="speakAnswer()" style="
            padding: 0.6rem 1rem;
            border-radius: 8px;
            border: 1px solid #cccccc;
            cursor: pointer;
            font-size: 15px;">
            🔊 Speak Bot Answer
        </button>

        <script>
        function speakAnswer() {{
            const text = {safe_text};
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "en-GB";
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """,
        height=70,
    )


def show_bot_result(result: dict) -> None:
    st.markdown("### Bot Answer")
    st.write(result["answer"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Confidence", result["confidence"])
    col2.metric("Fallback Used", "Yes" if result["fallback"] else "No")
    col3.metric(
        "Matched FAQ",
        result["matched_question"] if result["matched_question"] else "No reliable match",
    )

    st.markdown("### Voice Output")
    speak_answer_button(result["answer"])


init_db()
knowledge_base = load_knowledge_base()

if "customer_question" not in st.session_state:
    st.session_state.customer_question = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None


st.title("AI Customer Support Chatbot & Voicebot Automation Demo")

st.write(
    "This demo answers customer support questions from a small FAQ knowledge base, "
    "supports voice input, provides voice output, uses fallback handling when confidence is low, "
    "and logs conversations for monitoring."
)

tab_chat, tab_dashboard, tab_kb = st.tabs(
    ["Chatbot & Voicebot", "Monitoring Dashboard", "Knowledge Base"]
)


with tab_chat:
    st.subheader("Ask a customer support question")

    st.markdown("### Voice Input")
    st.write(
        "Click the voice button, speak your question, then review the transcribed text below."
    )

    voice_text = speech_to_text(
        language="en-GB",
        start_prompt="🎙️ Start Voice Input",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        key="voice_input",
    )

    if voice_text:
        st.session_state.customer_question = voice_text
        st.session_state.last_result = None
        st.success(f"Transcribed voice input: {voice_text}")
        st.info("Review the transcribed question, edit it if needed, then click Ask Bot.")

    st.markdown("### Text Input")

    user_question = st.text_input(
        "Customer question",
        placeholder="Example: How can I track my order?",
        key="customer_question",
    )

    ask_clicked = st.button("Ask Bot")

    if ask_clicked:
        if not user_question.strip():
            st.warning("Please enter or record a question.")
        else:
            result = find_best_answer(user_question, knowledge_base)

            save_conversation(
                user_question=user_question,
                bot_answer=result["answer"],
                confidence=result["confidence"],
                fallback=result["fallback"],
                matched_question=result["matched_question"],
            )

            st.session_state.last_result = result
            show_bot_result(result)

    elif st.session_state.last_result is not None:
        st.markdown("### Last Bot Answer")
        show_bot_result(st.session_state.last_result)


with tab_dashboard:
    st.subheader("Conversation Monitoring")

    rows = get_conversations()

    if not rows:
        st.info("No conversations logged yet.")
    else:
        df = pd.DataFrame(
            rows,
            columns=[
                "Timestamp",
                "User Question",
                "Bot Answer",
                "Confidence",
                "Fallback",
                "Matched Question",
            ],
        )

        total_chats = len(df)
        fallback_count = int(df["Fallback"].sum())
        avg_confidence = round(df["Confidence"].mean(), 2)
        fallback_rate = round((fallback_count / total_chats) * 100, 1)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Conversations", total_chats)
        col2.metric("Fallback Count", fallback_count)
        col3.metric("Fallback Rate", f"{fallback_rate}%")
        col4.metric("Average Confidence", avg_confidence)

        st.markdown("### Recent Conversations")
        st.dataframe(df, use_container_width=True)


with tab_kb:
    st.subheader("Current Knowledge Base")

    kb_df = pd.DataFrame(knowledge_base)
    st.dataframe(kb_df, use_container_width=True)

    st.markdown("### What this knowledge base demonstrates")
    st.write(
        "This demo uses FAQ similarity matching to simulate a small business customer "
        "support assistant. The bot retrieves the closest FAQ answer, assigns a "
        "confidence score, and falls back when the match is weak."
    )

    st.markdown("### Current limitations")
    st.write(
        "This MVP does not yet support PDF upload, CRM integration, WhatsApp integration, "
        "or advanced RAG. Those features can be added later for the freelance version."
    )