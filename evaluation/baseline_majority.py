import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "evaluation" / "golden_set.csv"


def main():
    df = pd.read_csv(CSV_PATH)

    # Remove rows without a valid intent
    df = df[df["intent"].notna()].copy()

    # Find the most common intent
    majority_intent = df["intent"].value_counts().idxmax()

    # Predict the majority class for every example
    predictions = [majority_intent] * len(df)

    accuracy = accuracy_score(
        df["intent"],
        predictions
    )

    print("=" * 60)
    print("MAJORITY CLASS BASELINE")
    print("=" * 60)

    print(f"\nNumber of examples: {len(df)}")
    print(f"Majority intent: {majority_intent}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")
    print(
        classification_report(
            df["intent"],
            predictions,
            zero_division=0
        )
    )


if __name__ == "__main__":
    main()
