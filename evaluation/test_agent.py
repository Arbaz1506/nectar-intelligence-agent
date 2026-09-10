import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.agent import classify_intent


test_messages = [
    "My Spotify app keeps crashing after the update.",
    "I was charged twice for Spotify Premium.",
    "I can't log into my Spotify account.",
    "How do I create a playlist?",
    "I want to get the student discount.",
    "My songs keep pausing while playing.",
    "I have some feedback about Spotify.",
    "Is there a way to see lyrics on Spotify?",
    "Something is wrong with my Spotify experience.",
]


for message in test_messages:
    intent, confidence = classify_intent(message)

    print("Message:", message)
    print("Intent:", intent)
    print("Confidence:", confidence)
    print()
