import json
import re

from rapidfuzz import fuzz


STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were",
    "i", "me", "my", "mine", "you", "your", "yours",
    "we", "our", "ours", "they", "their",
    "how", "what", "when", "where", "why", "who",
    "can", "could", "would", "should", "do", "does", "did",
    "to", "for", "from", "of", "in", "on", "at", "by", "with",
    "and", "or", "but", "if", "then", "please",
    "help", "problem", "issue", "question", "support", "solve"
}


def load_knowledge_base(file_path: str = "knowledge_base.json") -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_meaningful_tokens(text: str) -> set[str]:
    normalized = normalize_text(text)
    tokens = normalized.split()
    return {
        token
        for token in tokens
        if token not in STOPWORDS and len(token) > 2
    }


def fallback_response(confidence: float) -> dict:
    return {
        "answer": "I could not find a reliable answer. Please contact support.",
        "confidence": confidence,
        "fallback": True,
        "matched_question": None,
    }


def find_best_answer(user_question: str, knowledge_base: list[dict]) -> dict:
    user_question_clean = normalize_text(user_question)
    user_tokens = get_meaningful_tokens(user_question)

    if not user_tokens:
        return fallback_response(0.0)

    best_match = None
    best_score = 0.0
    best_overlap_count = 0

    for item in knowledge_base:
        faq_question = item["question"]
        faq_question_clean = normalize_text(faq_question)
        faq_tokens = get_meaningful_tokens(faq_question)

        fuzzy_score = fuzz.token_set_ratio(
            user_question_clean,
            faq_question_clean
        )

        overlap_tokens = user_tokens.intersection(faq_tokens)
        overlap_count = len(overlap_tokens)

        if user_tokens and faq_tokens:
            overlap_ratio = overlap_count / min(len(user_tokens), len(faq_tokens))
        else:
            overlap_ratio = 0.0

        combined_score = (0.55 * fuzzy_score) + (0.45 * overlap_ratio * 100)

        if combined_score > best_score:
            best_score = combined_score
            best_match = item
            best_overlap_count = overlap_count

    confidence = round(best_score / 100, 2)

    if best_match is None:
        return fallback_response(confidence)

    if best_overlap_count == 0:
        return fallback_response(confidence)

    if confidence < 0.60:
        return fallback_response(confidence)

    return {
        "answer": best_match["answer"],
        "confidence": confidence,
        "fallback": False,
        "matched_question": best_match["question"],
    }