# AI Customer Support Chatbot & Voicebot Automation Demo

A practical customer support chatbot and voicebot MVP built with Python and Streamlit.

The project demonstrates how a small business can automate basic customer support questions using a structured FAQ knowledge base, browser-based voice input, text-to-speech output, fallback handling, and conversation monitoring.

## Live Demo

Streamlit App:
https://ai-customer-support-chatbot-voicebot-demo.streamlit.app/

GitHub Repository:
https://github.com/yasirsiddiq01/ai-customer-support-chatbot-voicebot-demo

## Features

* Text-based customer support chatbot
* Browser-based voice input
* Browser text-to-speech output
* FAQ-based knowledge retrieval
* Confidence scoring
* Safer fallback handling for weak or vague questions
* SQLite conversation logging
* Monitoring dashboard
* Knowledge base viewer
* Simple deployment through Streamlit Community Cloud

## Demo Use Case

The demo simulates a customer support assistant for a small business.

It can answer common questions such as:

* How can I track my order?
* Can I cancel my order?
* What is your refund policy?
* Do you offer international shipping?
* Can I change my delivery address?
* How do I contact customer support?

If the user asks a vague or unsupported question, the bot does not invent an answer. It uses a fallback response:

> I could not find a reliable answer. Please contact support.

## Why This Project Matters

Many small businesses receive repeated customer questions about orders, refunds, delivery, and support. This project shows how a lightweight chatbot and voicebot can reduce repetitive support work while keeping fallback controls in place for questions outside the knowledge base.

The project is intentionally simple and explainable. It focuses on workflow, reliability, monitoring, and deployment rather than unnecessary complexity.

## Tech Stack

* Python
* Streamlit
* Pandas
* SQLite
* RapidFuzz
* streamlit-mic-recorder
* Browser Speech Recognition
* Browser Text-to-Speech
* GitHub
* Streamlit Community Cloud

## Project Architecture

```text
User text or voice input
        ↓
Speech-to-text transcription
        ↓
FAQ matching and confidence scoring
        ↓
Fallback decision
        ↓
Bot answer
        ↓
Text-to-speech output
        ↓
Conversation log saved to SQLite
        ↓
Monitoring dashboard
```

## Fallback Logic

The chatbot does not rely only on loose fuzzy matching. It also checks meaningful keyword overlap.

This reduces false answers for vague questions such as:

```text
How can I solve my problem?
```

Instead of guessing, the bot returns a fallback response.

## Current Limitations

This is an MVP demo, not a production system.

Current limitations:

* Voice input depends on browser speech recognition quality
* No PDF/document upload yet
* No WhatsApp integration yet
* No CRM integration yet
* No human handoff workflow yet
* No advanced RAG pipeline yet
* No authentication or user management

## Future Improvements

Planned freelance-ready improvements:

* PDF and document-based knowledge base upload
* OpenAI Whisper or stronger speech-to-text
* Advanced RAG with embeddings
* Admin dashboard for editing FAQs
* WhatsApp or website widget integration
* Human handoff to email or CRM
* Lead capture and follow-up automation
* Multilingual support
* Client-ready analytics dashboard

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Repository Structure

```text
app.py                 Main Streamlit application
chatbot.py             FAQ matching and fallback logic
database.py            SQLite logging functions
knowledge_base.json    Sample FAQ knowledge base
requirements.txt       Python dependencies
README.md              Project documentation
.gitignore             Files excluded from Git
```

## Portfolio Relevance

This project demonstrates practical skills in:

* Conversational AI workflow design
* Chatbot and voicebot prototyping
* FAQ knowledge-base automation
* Fallback and reliability controls
* Monitoring and conversation logging
* Python application development
* Streamlit deployment
* Client-facing AI automation demos

## Author

Yasir Siddiq
GitHub: https://github.com/yasirsiddiq01
Streamlit Demo: https://ai-customer-support-chatbot-voicebot-demo.streamlit.app/
