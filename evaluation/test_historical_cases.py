import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.historical_cases import build_spotify_cases


DATA_PATH = "data/raw/archive/twcs/twcs.csv"


cases = build_spotify_cases(DATA_PATH)

print("Total historical cases:", len(cases))

print("\nSample cases:\n")
print(
    cases[
        [
            "customer_message",
            "historical_reply",
        ]
    ].head(10).to_string(index=False)
)


cases.to_csv("evaluation/historical_cases.csv", index=False)
