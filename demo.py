from src.agent import run_agent


def display_result(result):
    """Display the NIA agent result in a readable format."""

    print("\n" + "=" * 70)
    print("NIA ANALYSIS")
    print("=" * 70)

    print(f"Intent       : {result['intent']}")
    print(f"Confidence   : {result['confidence']:.3f}")
    print(f"Grounded     : {result['grounded']}")
    print(f"Similarity   : {result['similarity']:.3f}")
    print(f"Escalated    : {result['escalated']}")

    if result["escalation_reason"]:
        print(f"Reason       : {result['escalation_reason']}")

    print("\n" + "-" * 70)
    print("NIA RESPONSE")
    print("-" * 70)

    if result["reply"]:
        print(result["reply"])
    else:
        print("No grounded response available. Escalation required.")

    if result["evidence"]:
        print("\n" + "-" * 70)
        print("RETRIEVED HISTORICAL EVIDENCE")
        print("-" * 70)

        for i, evidence in enumerate(result["evidence"], start=1):
            print(f"\nEvidence {i}")
            print(f"Similarity : {evidence['similarity']:.3f}")
            print(f"Customer   : {evidence['customer_message']}")
            print(f"Historical : {evidence['historical_reply']}")


def main():
    print("=" * 70)
    print("NIA — Nectar Intelligence Assistant")
    print("=" * 70)

    print("\nNIA analyzes Spotify customer-support messages using:")
    print("• Intent classification")
    print("• Historical case retrieval")
    print("• Evidence grounding")
    print("• Escalation for unsupported queries")

    print("\nType 'exit' to quit.")

    while True:
        print("\n" + "-" * 70)

        query = input("Customer: ").strip()

        if query.lower() == "exit":
            print("\nThank you for using NIA.")
            break

        if not query:
            print("Please enter a customer message.")
            continue

        try:
            result = run_agent(query)
            display_result(result)

        except Exception as error:
            print("\nError while processing the request:")
            print(error)


if __name__ == "__main__":
    main()
