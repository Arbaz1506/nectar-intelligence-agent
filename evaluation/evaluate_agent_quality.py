import sys
import os
import pandas as pd

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from src.agent import run_agent


# --------------------------------------------------
# TEST CASES
# --------------------------------------------------

TEST_CASES = [
    {
        "query": "Spotify app keeps crashing when I open it",
        "expected_grounded": True,
        "expected_escalation": False,
    },
    {
        "query": "I was charged twice for Spotify Premium",
        "expected_grounded": True,
        "expected_escalation": False,
    },
    {
        "query": "I cannot log into my Spotify account",
        "expected_grounded": True,
        "expected_escalation": False,
    },
    {
        "query": "My Spotify playlist disappeared",
        "expected_grounded": True,
        "expected_escalation": False,
    },
    {
        "query": "How do I get the Spotify student discount?",
        "expected_grounded": True,
        "expected_escalation": False,
    },
    {
        "query": "How do I create a Spotify family plan?",
        "expected_grounded": False,
        "expected_escalation": True,
    },
    {
        "query": "I cannot play songs on Spotify",
        "expected_grounded": False,
        "expected_escalation": True,
    },
    {
        "query": "What is the weather going to be tomorrow?",
        "expected_grounded": False,
        "expected_escalation": True,
    },
    {
        "query": "How do I make pancakes?",
        "expected_grounded": False,
        "expected_escalation": True,
    },
    {
        "query": "What is the capital of France?",
        "expected_grounded": False,
        "expected_escalation": True,
    },
]


# --------------------------------------------------
# RUN EVALUATION
# --------------------------------------------------

print("=" * 80)
print("NIA AGENT QUALITY EVALUATION")
print("=" * 80)


results = []


for case in TEST_CASES:

    query = case["query"]

    result = run_agent(query)

    grounded = result["grounded"]
    escalated = result["escalated"]

    print("\n" + "-" * 80)
    print(f"QUERY: {query}")

    print(f"Intent: {result['intent']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Grounded: {grounded}")
    print(f"Similarity: {result['similarity']:.3f}")
    print(f"Escalated: {escalated}")

    if result["escalation_reason"]:
        print(
            f"Escalation reason: "
            f"{result['escalation_reason']}"
        )

    print(f"Reply: {result['reply']}")

    grounded_correct = (
        grounded == case["expected_grounded"]
    )

    escalation_correct = (
        escalated == case["expected_escalation"]
    )

    results.append(
        {
            "query": query,
            "intent": result["intent"],
            "confidence": result["confidence"],
            "grounded": grounded,
            "similarity": result["similarity"],
            "escalated": escalated,
            "escalation_reason": result["escalation_reason"],
            "reply": result["reply"],
            "expected_grounded": case["expected_grounded"],
            "expected_escalation": case["expected_escalation"],
            "grounded_correct": grounded_correct,
            "escalation_correct": escalation_correct,
        }
    )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

df = pd.DataFrame(results)

grounded_accuracy = df["grounded_correct"].mean()
escalation_accuracy = df["escalation_correct"].mean()


print("\n" + "=" * 80)
print("QUALITY SUMMARY")
print("=" * 80)

print(
    f"Grounding accuracy: "
    f"{grounded_accuracy:.2f}"
)

print(
    f"Escalation accuracy: "
    f"{escalation_accuracy:.2f}"
)

print(
    f"Correct grounded decisions: "
    f"{df['grounded_correct'].sum()}/{len(df)}"
)

print(
    f"Correct escalation decisions: "
    f"{df['escalation_correct'].sum()}/{len(df)}"
)


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

OUTPUT_PATH = "evaluation/agent_quality_results.csv"

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nResults saved to:")
print(OUTPUT_PATH)
