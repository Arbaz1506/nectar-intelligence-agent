import re
from typing import Tuple

from src.retrieval import HistoricalRetriever


INTENT_KEYWORDS = {
    "premium_subscription": [
        "premium",
        "upgrade",
        "downgrade",
        "premium account",
        "premium plan",
    ],
    "student_plan": [
        "student",
        "student discount",
        "student plan",
        "unidays",
    ],
    "family_plan": [
        "family",
        "family plan",
        "family account",
        "family members",
    ],
    "billing_payment": [
        "charged",
        "charge",
        "payment",
        "billing",
        "refund",
        "price",
        "invoice",
        "double charged",
        "charged twice",
    ],
    "account_login_security": [
        "login",
        "log in",
        "sign in",
        "password",
        "account",
        "username",
        "locked out",
        "can't access",
    ],
    "app_technical_issue": [
        "app",
        "crash",
        "crashing",
        "not working",
        "bug",
        "error",
        "freeze",
        "frozen",
        "update",
        "loading",
    ],
    "playback_music_issue": [
        "play",
        "playing",
        "song",
        "music",
        "track",
        "pause",
        "paused",
        "skip",
        "shuffle",
        "repeat",
        "audio",
    ],
    "playlist_library": [
        "playlist",
        "library",
        "saved songs",
        "liked songs",
        "album",
        "albums",
    ],
    "feature_information": [
        "how do i",
        "is there a way",
        "can i",
        "feature",
        "available",
        "support",
        "does spotify",
    ],
}


def _normalize(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def classify_intent(text: str) -> Tuple[str, float]:
    """
    Classify a customer message using keyword matching.

    Returns:
        (intent, confidence)
    """

    text = _normalize(text)

    scores = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if re.search(
                r"\b" + re.escape(keyword) + r"\b",
                text
            ):
                score += 1

        scores[intent] = score

    best_intent = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_intent]

    if best_score == 0:
        return "feedback_other", 0.0

    total_matches = sum(scores.values())

    confidence = best_score / total_matches

    return best_intent, round(confidence, 3)


# ==========================================================
# HISTORICAL RETRIEVAL
# ==========================================================

CASES_PATH = "evaluation/historical_cases.csv"

retriever = HistoricalRetriever(CASES_PATH)


# ==========================================================
# EVIDENCE-BASED REPLY
# ==========================================================

def generate_reply(
    text: str,
    top_k: int = 3,
    min_similarity: float = 0.6,
) -> dict:
    """
    Retrieve historical customer-support evidence
    and return the best grounded reply.
    """

    results = retriever.search(
        text,
        top_k=top_k,
        min_similarity=min_similarity,
    )

    if results.empty:
        return {
            "reply": None,
            "evidence": [],
            "grounded": False,
        }

    best_match = results.iloc[0]

    return {
        "reply": best_match["historical_reply"],
        "evidence": results[
            [
                "customer_message",
                "historical_reply",
                "similarity",
            ]
        ].to_dict("records"),
        "grounded": True,
    }
    
def should_escalate(
    intent: str,
    confidence: float,
    grounded: bool,
    similarity: float = 0.0,
) -> Tuple[bool, str]:
    """
    Decide whether a customer message should be escalated
    instead of receiving an automated grounded response.
    """

    if confidence < 0.5:
        return True, "Low intent classification confidence."

    if not grounded:
        return True, "No sufficiently similar historical evidence found."

    if similarity < 0.6:
        return True, "Historical evidence similarity is below the required threshold."

    return False, ""
def run_agent(
    text: str,
    top_k: int = 3,
    min_similarity: float = 0.6,
) -> dict:
    """
    Run the complete NIA agent pipeline.

    Pipeline:
        1. Classify intent
        2. Retrieve historical evidence
        3. Generate grounded reply
        4. Decide whether to escalate
    """

    intent, confidence = classify_intent(text)

    reply_result = generate_reply(
        text,
        top_k=top_k,
        min_similarity=min_similarity,
    )

    best_similarity = 0.0

    if reply_result["evidence"]:
        best_similarity = reply_result["evidence"][0]["similarity"]

    escalated, escalation_reason = should_escalate(
        intent=intent,
        confidence=confidence,
        grounded=reply_result["grounded"],
        similarity=best_similarity,
    )

    return {
        "message": text,
        "intent": intent,
        "confidence": confidence,
        "reply": reply_result["reply"],
        "grounded": reply_result["grounded"],
        "similarity": round(best_similarity, 3),
        "evidence": reply_result["evidence"],
        "escalated": escalated,
        "escalation_reason": escalation_reason,
    }
