import json
from rapidfuzz import fuzz


def load_knowledge_base(file_path: str = "knowledge_base.json") -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_best_answer(user_question: str, knowledge_base: list[dict]) -> dict:
    best_match = None
    best_score = 0

    for item in knowledge_base:
        score = fuzz.token_set_ratio(user_question.lower(), item["question"].lower())

        if score > best_score:
            best_score = score
            best_match = item

    confidence = round(best_score / 100, 2)

    if confidence < 0.55:
        return {
            "answer": "I could not find a reliable answer. Please contact support.",
            "confidence": confidence,
            "fallback": True,
            "matched_question": None
        }

    return {
        "answer": best_match["answer"],
        "confidence": confidence,
        "fallback": False,
        "matched_question": best_match["question"]
    }