import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "evaluation" / "golden_set.csv"


def main():
    # Load golden set
    df = pd.read_csv(CSV_PATH)

    # Keep only valid rows
    df = df[
        df["text"].notna() &
        df["intent"].notna()
    ].copy()

    X = df["text"].astype(str)
    y = df["intent"].astype(str)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    # TF-IDF + Logistic Regression
    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
            ),
        ),
    ])

    # Train
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)

    # Metrics
    accuracy = accuracy_score(y_test, predictions)

    print("=" * 60)
    print("TF-IDF + LOGISTIC REGRESSION BASELINE")
    print("=" * 60)

    print(f"\nTraining examples: {len(X_train)}")
    print(f"Test examples:     {len(X_test)}")

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )


if __name__ == "__main__":
    main()
