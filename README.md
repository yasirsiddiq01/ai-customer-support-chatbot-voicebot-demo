# AI Customer Support Chatbot & Voicebot Automation Demo

This project is a small customer support chatbot and voicebot demo built for AI automation portfolio work.

The demo answers customer support questions from a small FAQ knowledge base, supports browser-based voice input, provides browser text-to-speech output, uses fallback handling when confidence is low, and logs conversations for monitoring.

## Features

- Text-based customer support chatbot
- Browser-based voice input
- Browser text-to-speech output
- FAQ-based knowledge retrieval
- Confidence scoring
- Fallback handling for weak matches
- SQLite conversation logging
- Monitoring dashboard
- Knowledge base viewer
- Docker-ready deployment

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- RapidFuzz
- streamlit-mic-recorder
- Docker

## Demo Use Case

A small business wants to automate basic customer support questions such as:

- Order tracking
- Refund policy
- Business hours
- Delivery address changes
- International shipping
- Bulk order discounts

The bot retrieves the closest FAQ answer and falls back when it cannot find a reliable match.

## Current Limitations

This is an MVP demo. It does not yet include:

- PDF or document upload
- WhatsApp integration
- CRM integration
- Advanced RAG
- Production-grade speech-to-text
- User authentication
- Human handoff workflow

These features can be added in the freelance version.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt