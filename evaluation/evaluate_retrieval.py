import sys
import os
import pandas as pd

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from src.retrieval import HistoricalRetriever


CASES_PATH = "evaluation/historical_cases.csv"

retriever = HistoricalRetriever(CASES_PATH)


# --------------------------------------------------
# TEST CASES
# --------------------------------------------------

TEST_CASES = [
    {
        "query": "Spotify app keeps crashing when I open it",
        "expected_evidence": True,
    },
    {
        "query": "I was charged twice for Spotify Premium",
        "expected_evidence": True,
    },
    {
        "query": "I cannot log into my Spotify account",
        "expected_evidence": True,
    },
    {
        "query": "My Spotify playlist disappeared",
        "expected_evidence": True,
    },
    {
        "query": "My Spotify Premium subscription is not working",
        "expected_evidence": True,
    },
    {
        "query": "I cannot play songs on Spotify",
        "expected_evidence": True,
    },
    {
        "query": "How do I get the Spotify student discount?",
        "expected_evidence": True,
    },
    {
        "query": "How do I create a Spotify family plan?",
        "expected_evidence": True,
    },
    {
        "query": "What is the weather going to be tomorrow?",
        "expected_evidence": False,
    },
    {
        "query": "How do I make pancakes?",
        "expected_evidence": False,
    },
    {
        "query": "What is the capital of France?",
        "expected_evidence": False,
    },
    {
        "query": "Tell me a joke about computers",
        "expected_evidence": False,
    },
]


# --------------------------------------------------
# EVALUATE SINGLE QUERY
# --------------------------------------------------

def evaluate_query(query, expected_evidence):

    results = retriever.search(
        query,
        top_k=3,
        min_similarity=0.6
    )

    has_evidence = not results.empty

    print("\n" + "-" * 80)
    print(f"QUERY: {query}")
    print(f"Expected evidence: {expected_evidence}")
    print(f"Retrieved evidence: {has_evidence}")

    if has_evidence:

        print("\nTop retrieved cases:")

        for i, (_, result) in enumerate(
            results.iterrows(),
            start=1
        ):

            print(
                f"\n{i}. Similarity: "
                f"{result['similarity']:.3f}"
            )

            print(
                f"Customer: "
                f"{result['customer_message']}"
            )

            print(
                f"Historical reply: "
                f"{result['historical_reply']}"
            )

    return has_evidence


# --------------------------------------------------
# MAIN EVALUATION
# --------------------------------------------------

print("=" * 80)
print("NIA RETRIEVAL EVALUATION")
print("=" * 80)

correct = 0
false_positives = 0
false_negatives = 0

rows = []


for case in TEST_CASES:

    actual = evaluate_query(
        case["query"],
        case["expected_evidence"]
    )

    expected = case["expected_evidence"]

    if actual == expected:
        correct += 1

    elif actual and not expected:
        false_positives += 1

    elif not actual and expected:
        false_negatives += 1

    rows.append(
        {
            "query": case["query"],
            "expected_evidence": expected,
            "retrieved_evidence": actual,
            "correct": actual == expected,
        }
    )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

accuracy = correct / len(TEST_CASES)


print("\n" + "=" * 80)
print("RETRIEVAL SUMMARY")
print("=" * 80)

print(f"Total test cases: {len(TEST_CASES)}")
print(f"Correct: {correct}")
print(f"Accuracy: {accuracy:.2f}")
print(f"False positives: {false_positives}")
print(f"False negatives: {false_negatives}")


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

OUTPUT_PATH = "evaluation/retrieval_results.csv"

pd.DataFrame(rows).to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nResults saved to:")
print(OUTPUT_PATH)
