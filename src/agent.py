import re
from typing import Tuple

from src.retrieval import HistoricalRetriever


# ==========================================================
# INTENT KEYWORDS
# ==========================================================

INTENT_KEYWORDS = {
    "premium_subscription": [
        "premium",
        "upgrade",
        "downgrade",
        "premium account",
        "premium plan",
        "subscription",
        "subscribe",
        "cancel premium",
    ],

    "student_plan": [
        "student",
        "student discount",
        "student plan",
        "student premium",
        "student subscription",
        "student offer",
        "unidays",
    ],

    "family_plan": [
        "family",
        "family plan",
        "family account",
        "family members",
        "family subscription",
    ],

    "billing_payment": [
        "charged",
        "charge",
        "payment",
        "billing",
        "refund",
        "price",
        "invoice",
        "charged twice",
        "double charged",
        "payment failed",
        "payment declined",
        "wrong charge",
    ],

    "account_login_security": [
        "login",
        "log in",
        "login",
        "sign in",
        "password",
        "account",
        "username",
        "locked out",
        "can't access",
        "cannot access",
        "hacked",
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
        "overheating",
        "overheat",
        "sync",
        "out of sync",
        "doesn't work",
        "wont work",
        "won't work",
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
        "listen",
        "playback",
        "stops playing",
        "can't play",
        "cannot play",
        "won't play",
    ],

    "playlist_library": [
        "playlist",
        "library",
        "saved songs",
        "liked songs",
        "liked music",
        "album",
        "albums",
        "playlist missing",
        "playlist disappeared",
        "playlist gone",
        "library missing",
        "songs disappeared",
    ],

    "feature_information": [
        "lyrics",
        "in rotation",
        "discover weekly",
        "release radar",
        "spotify connect",
        "voice control",
        "offline mode",
        "crossfade",
        "equalizer",
        "podcast",
        "podcasts",
        "feature",
        "available",
        "how can i use",
        "how do i use",
        "is there a way",
        "does spotify have",
        "does spotify support",
        "can spotify",
    ],
}


# ==========================================================
# STRONG INTENT KEYWORDS
# ==========================================================

INTENT_STRONG_KEYWORDS = {
    "premium_subscription": [
        "upgrade to premium",
        "premium subscription",
        "premium plan",
        "premium account",
        "cancel premium",
        "downgrade premium",
        "spotify premium",
    ],

    "student_plan": [
        "student discount",
        "student plan",
        "student premium",
        "student subscription",
        "student offer",
        "student spotify",
        "unidays",
    ],

    "family_plan": [
        "family plan",
        "family account",
        "family subscription",
        "family members",
        "spotify family",
    ],

    "billing_payment": [
        "charged twice",
        "charged me",
        "double charged",
        "payment failed",
        "payment declined",
        "refund",
        "billing issue",
        "wrong charge",
        "charged for",
        "money taken",
    ],

    "account_login_security": [
        "can't log in",
        "cannot log in",
        "can't login",
        "cannot login",
        "can't sign in",
        "cannot sign in",
        "forgot password",
        "reset password",
        "locked out",
        "hacked account",
        "account hacked",
    ],

    "app_technical_issue": [
        "app keeps crashing",
        "app is crashing",
        "app crashes",
        "app won't open",
        "app won't load",
        "app not working",
        "app stopped working",
        "app freezes",
        "app is frozen",
        "technical issue",
        "error message",
        "keeps crashing",
        "keeps freezing",
        "out of sync",
        "overheating",
    ],

    "playback_music_issue": [
        "can't play",
        "cannot play",
        "won't play",
        "stops playing",
        "keeps pausing",
        "music stops",
        "song won't play",
        "songs won't play",
        "playback issue",
        "can't listen",
        "cannot listen",
    ],

    "playlist_library": [
        "playlist disappeared",
        "playlist missing",
        "lost my playlist",
        "playlist not showing",
        "liked songs disappeared",
        "library disappeared",
        "can't find my playlist",
        "songs disappeared",
    ],

    "feature_information": [
        "is there a way",
        "can spotify",
        "does spotify have",
        "does spotify support",
        "how can i use",
        "how do i use",
        "spotify feature",
        "new feature",
        "feature available",
    ],
}


# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def _normalize(text: str) -> str:
    text = str(text).lower()

    text = text.replace(
        "&amp;",
        "and"
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================================
# INTENT CLASSIFICATION
# ==========================================================

def classify_intent(text: str) -> Tuple[str, float]:
    """
    Classify a customer message using weighted keyword matching.

    Strong intent-specific phrases receive higher weight than
    generic keywords.
    """

    text = _normalize(text)

    scores = {
        intent: 0
        for intent in INTENT_KEYWORDS
    }

    # ------------------------------------------------------
    # Generic keyword matches
    # ------------------------------------------------------

    for intent, keywords in INTENT_KEYWORDS.items():

        for keyword in keywords:

            if re.search(
                r"\b" + re.escape(keyword) + r"\b",
                text
            ):
                scores[intent] += 1

    # ------------------------------------------------------
    # Strong keyword matches
    # ------------------------------------------------------

    for intent, keywords in INTENT_STRONG_KEYWORDS.items():

        for keyword in keywords:

            if re.search(
                r"\b" + re.escape(keyword) + r"\b",
                text
            ):
                scores[intent] += 3

    # ------------------------------------------------------
    # Special handling for unrelated/general messages
    # ------------------------------------------------------

    spotify_context = any(
        term in text
        for term in [
            "spotify",
            "premium",
            "playlist",
            "song",
            "music",
            "album",
            "track",
            "app",
        ]
    )

    if not spotify_context:
        return "feedback_other", 0.0

    # ------------------------------------------------------
    # Best intent
    # ------------------------------------------------------

    best_intent = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_intent]

    if best_score == 0:
        return "feedback_other", 0.0

    # ------------------------------------------------------
    # Confidence
    # ------------------------------------------------------

    total_score = sum(
        scores.values()
    )

    confidence = (
        best_score / total_score
        if total_score > 0
        else 0.0
    )

    return (
        best_intent,
        round(confidence, 3)
    )


# ==========================================================
# HISTORICAL RETRIEVER
# ==========================================================

CASES_PATH = "evaluation/historical_cases.csv"

retriever = HistoricalRetriever(
    CASES_PATH
)


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


# ==========================================================
# ESCALATION LOGIC
# ==========================================================

def should_escalate(
    intent: str,
    confidence: float,
    grounded: bool,
    similarity: float = 0.0,
) -> Tuple[bool, str]:

    if confidence < 0.5:

        return (
            True,
            "Low intent classification confidence."
        )

    if not grounded:

        return (
            True,
            "No sufficiently similar historical evidence found."
        )

    if similarity < 0.6:

        return (
            True,
            "Historical evidence similarity is below the required threshold."
        )

    return False, ""


# ==========================================================
# COMPLETE NIA AGENT
# ==========================================================

def run_agent(
    text: str,
    top_k: int = 3,
    min_similarity: float = 0.6,
) -> dict:
    """
    Run the complete NIA agent pipeline.
    """

    intent, confidence = classify_intent(
        text
    )

    reply_result = generate_reply(
        text,
        top_k=top_k,
        min_similarity=min_similarity,
    )

    best_similarity = 0.0

    if reply_result["evidence"]:

        best_similarity = (
            reply_result["evidence"][0]["similarity"]
        )

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
        "similarity": round(
            best_similarity,
            3
        ),
        "evidence": reply_result["evidence"],
        "escalated": escalated,
        "escalation_reason": escalation_reason,
    }
