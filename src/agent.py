import re
from typing import Tuple


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
           if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                score += 1

        scores[intent] = score

    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    if best_score == 0:
        return "feedback_other", 0.0

    total_matches = sum(scores.values())

    confidence = best_score / total_matches

    return best_intent, round(confidence, 3)
