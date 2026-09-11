import sys
import os

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.agent import classify_intent


# ==========================================================
# LOAD GOLDEN SET
# ==========================================================

GOLDEN_PATH = "evaluation/golden_set.csv"

golden = pd.read_csv(GOLDEN_PATH)

print("\n==============================")
print("NIA AGENT EVALUATION")
print("==============================")

print("\nGolden set size:")
print(len(golden))


# ==========================================================
# RUN INTENT CLASSIFIER
# ==========================================================

predictions = []

for text in golden["text"]:

    intent, confidence = classify_intent(text)

    predictions.append(intent)


golden["predicted_intent"] = predictions


# ==========================================================
# ACCURACY
# ==========================================================

accuracy = accuracy_score(
    golden["intent"],
    golden["predicted_intent"],
)


print("\nIntent Accuracy:")
print(round(accuracy, 4))


# ==========================================================
# CLASSIFICATION REPORT
# ==========================================================

print("\nClassification Report:\n")

print(
    classification_report(
        golden["intent"],
        golden["predicted_intent"],
        zero_division=0,
    )
)


# ==========================================================
# SAVE RESULTS
# ==========================================================

OUTPUT_PATH = "evaluation/agent_intent_results.csv"

golden.to_csv(
    OUTPUT_PATH,
    index=False,
)

print("\nResults saved to:")
print(OUTPUT_PATH)


# ==========================================================
# MISCLASSIFIED EXAMPLES
# ==========================================================

misclassified = golden[
    golden["intent"] != golden["predicted_intent"]
]

print("\n==============================")
print("MISCLASSIFIED EXAMPLES")
print("==============================")

print("\nTotal misclassified:")
print(len(misclassified))

print("\nSample misclassified examples:\n")

print(
    misclassified[
        [
            "text",
            "intent",
            "predicted_intent",
        ]
    ].head(20).to_string(index=False)
)


# ==========================================================
# CONFUSION MATRIX
# ==========================================================

labels = sorted(
    golden["intent"].unique()
)

cm = confusion_matrix(
    golden["intent"],
    golden["predicted_intent"],
    labels=labels,
)

confusion_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels,
)

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")

print(confusion_df)
