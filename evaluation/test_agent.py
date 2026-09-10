import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.agent import run_agent


# ==========================================================
# TEST 1: GROUNDED CUSTOMER ISSUE
# ==========================================================

message = "My Spotify app keeps crashing after the update."

result = run_agent(message)


print("\n==============================")
print("TEST 1: GROUNDED MESSAGE")
print("==============================")

print("\nCustomer message:")
print(result["message"])

print("\nIntent:")
print(result["intent"])

print("\nConfidence:")
print(result["confidence"])

print("\nSimilarity:")
print(result["similarity"])

print("\nGrounded:")
print(result["grounded"])

print("\nEscalated:")
print(result["escalated"])

print("\nEscalation reason:")
print(result["escalation_reason"])

print("\nReply:")
print(result["reply"])


# ==========================================================
# TEST 2: UNGROUNDED MESSAGE
# ==========================================================

message_2 = "How do I make pancakes?"

result_2 = run_agent(message_2)


print("\n==============================")
print("TEST 2: UNGROUNDED MESSAGE")
print("==============================")

print("\nCustomer message:")
print(result_2["message"])

print("\nIntent:")
print(result_2["intent"])

print("\nConfidence:")
print(result_2["confidence"])

print("\nSimilarity:")
print(result_2["similarity"])

print("\nGrounded:")
print(result_2["grounded"])

print("\nEscalated:")
print(result_2["escalated"])

print("\nEscalation reason:")
print(result_2["escalation_reason"])

print("\nReply:")
print(result_2["reply"])


# ==========================================================
# TEST 3: BILLING ISSUE
# ==========================================================

message_3 = "I was charged twice for Spotify Premium."

result_3 = run_agent(message_3)


print("\n==============================")
print("TEST 3: BILLING MESSAGE")
print("==============================")

print("\nCustomer message:")
print(result_3["message"])

print("\nIntent:")
print(result_3["intent"])

print("\nConfidence:")
print(result_3["confidence"])

print("\nSimilarity:")
print(result_3["similarity"])

print("\nGrounded:")
print(result_3["grounded"])

print("\nEscalated:")
print(result_3["escalated"])

print("\nEscalation reason:")
print(result_3["escalation_reason"])

print("\nReply:")
print(result_3["reply"])
