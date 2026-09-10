import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retrieval import HistoricalRetriever


CASES_PATH = "evaluation/historical_cases.csv"


retriever = HistoricalRetriever(CASES_PATH)


query = "My Spotify app keeps crashing after I updated it."


results = retriever.search(
    query,
    top_k=5,
    min_similarity=0.6,
)


print("\nQuery:")
print(query)

print("\nTop historical matches:\n")

for i, row in results.iterrows():
    print(f"--- Match {i + 1} ---")
    print("Similarity:", round(row["similarity"], 3))
    print("Customer:", row["customer_message"])
    print("Historical reply:", row["historical_reply"])
    print()

print("\nHas historical evidence:", retriever.has_evidence(query))
