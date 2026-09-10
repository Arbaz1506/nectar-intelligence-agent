import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import load_spotify_data


DATA_PATH = PROJECT_ROOT / "data" / "raw" / "archive" / "twcs" / "twcs.csv"
OUTPUT_PATH = PROJECT_ROOT / "evaluation" / "golden_set.csv"


def prepare_golden_set():
    spotify_df = load_spotify_data(DATA_PATH)

    customer_tweets = spotify_df[
        spotify_df["inbound"] == True
    ].copy()

    golden_set = customer_tweets[
        ["tweet_id", "author_id", "text", "created_at"]
    ].sample(
        n=200,
        random_state=2026
    ).reset_index(drop=True)

    golden_set["intent"] = ""
    golden_set["should_escalate"] = ""
    golden_set["escalation_reason"] = ""

    golden_set.to_csv(OUTPUT_PATH, index=False)

    print(f"Golden set created: {OUTPUT_PATH}")
    print(f"Examples: {len(golden_set)}")


if __name__ == "__main__":
    prepare_golden_set()
