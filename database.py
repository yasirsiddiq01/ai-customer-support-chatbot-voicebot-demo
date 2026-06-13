import sqlite3
from datetime import datetime


DB_NAME = "chat_logs.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_question TEXT NOT NULL,
            bot_answer TEXT NOT NULL,
            confidence REAL NOT NULL,
            fallback INTEGER NOT NULL,
            matched_question TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def save_conversation(user_question, bot_answer, confidence, fallback, matched_question):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (
            timestamp,
            user_question,
            bot_answer,
            confidence,
            fallback,
            matched_question
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(timespec="seconds"),
            user_question,
            bot_answer,
            confidence,
            int(fallback),
            matched_question
        )
    )

    conn.commit()
    conn.close()


def get_conversations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            timestamp,
            user_question,
            bot_answer,
            confidence,
            fallback,
            matched_question
        FROM conversations
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows