import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "evaluation" / "golden_set.csv"

INTENTS = {
    "1": "premium_subscription",
    "2": "family_plan",
    "3": "student_plan",
    "4": "billing_payment",
    "5": "account_login_security",
    "6": "app_technical_issue",
    "7": "playback_music_issue",
    "8": "playlist_library",
    "9": "feature_information",
    "0": "feedback_other",
}


def main():
    df = pd.read_csv(CSV_PATH)

    # Find first unlabeled example
    unlabeled = df[
        df["intent"].isna() |
        (df["intent"].astype(str).str.strip() == "")
    ]

    if unlabeled.empty:
        print("\nAll 200 examples are already labeled! 🎉")
        return

    print("\nNIA — Fast Golden Set Labeling")
    print("=" * 60)
    print(f"Remaining: {len(unlabeled)} / {len(df)}")
    print("\nKeyboard:")
    print("1-9 = intent")
    print("0   = feedback_other")
    print("Y   = escalate")
    print("N   = don't escalate")
    print("Q   = quit")
    print("=" * 60)

    for index, row in df.iterrows():

        if pd.notna(row["intent"]) and str(row["intent"]).strip():
            continue

        print("\n" + "-" * 60)
        print(f"Example {index + 1} / {len(df)}")
        print("-" * 60)
        print(row["text"])

        # Intent
        while True:
            choice = input("\nIntent [1-9/0]: ").strip()

            if choice in INTENTS:
                intent = INTENTS[choice]
                break

            if choice.lower() == "q":
                print("\nProgress saved. Exiting.")
                return

            print("Invalid choice.")

        # Escalation
        while True:
            choice = input("Escalate? [Y/N]: ").strip().lower()

            if choice in {"y", "n"}:
                should_escalate = choice == "y"
                break

            if choice == "q":
                print("\nProgress saved. Exiting.")
                return

            print("Enter Y or N.")

        # Reason
        if should_escalate:
            reason = input("Reason (short): ").strip()

            if not reason:
                reason = "requires human intervention"
        else:
            reason = "not needed"

        # Save
        df.at[index, "intent"] = intent
        df.at[index, "should_escalate"] = str(should_escalate).lower()
        df.at[index, "escalation_reason"] = reason

        df.to_csv(CSV_PATH, index=False)

        print("✓ Saved")

    print("\n" + "=" * 60)
    print("🎉 Golden set labeling complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
