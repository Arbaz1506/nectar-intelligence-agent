# NIA — Failure Analysis

## Overview

NIA was evaluated as a customer-support intelligence assistant using a
200-example golden set and a historical SpotifyCares support dataset.

The evaluation intentionally includes failure cases. The goal is not only
to measure accuracy, but also to understand where a lightweight
classification and retrieval pipeline can make incorrect decisions.

---

## 1. Intent Classification Failures

### Overall result

| Metric | Result |
|---|---:|
| Golden examples | 200 |
| Accuracy | 63% |
| Macro F1 | 0.51 |
| Weighted F1 | 0.62 |
| Misclassified examples | 74 |

The classifier performs best on the majority `feedback_other` class and
struggles more with smaller or semantically overlapping categories.

---

## 2. Feature Information vs Technical Issues

Example:

> "I don’t really use it whilst I’m at home... Voice control pops up all the time too."

Expected:

`app_technical_issue`

Predicted:

`feature_information`

### Why this happens

The message contains the explicit phrase "voice control", which is strongly
associated with Spotify features. However, the actual complaint is that
voice control appears unexpectedly, making this an application behavior
problem.

### Lesson

Keyword-based classification can confuse a feature being mentioned with
the actual intent of the customer.

A future improvement would use semantic classification or a trained
intent model that considers the relationship between the feature and the
customer's complaint.

---

## 3. Billing vs Other Intent

Example:

> "Now let's talk about lowering my payments 👀"

Expected:

`billing_payment`

Predicted:

`feedback_other`

### Why this happens

The message does not contain an explicit phrase such as "charged",
"payment failed", "refund", or "billing".

### Lesson

Short customer messages often lack enough explicit context for
keyword-based classification.

Conversation history or a semantic classifier would help recover the
intended meaning.

---

## 4. Student Plan vs Billing

Example:

> "trying to get around the student discount, but site crashed before I
> could finish... $ taken out"

Expected:

`billing_payment`

Predicted:

`student_plan`

### Why this happens

The phrase "student discount" is a strong signal for the student-plan
intent, while the actual customer problem includes a payment being taken
despite the failed process.

### Lesson

Messages can contain multiple valid intents. A single-label classifier
must decide which issue is the primary one.

A production system could support multi-intent detection or prioritize
high-risk intents such as billing and payment failures.

---

# Retrieval Failures

## 5. Lexical Similarity False Positive

Query:

> "I was charged twice for Spotify Premium"

Top retrieved historical case:

> "Why is twice not on Spotify....."

Similarity:

`0.735`

### Why this is a failure

The TF-IDF retriever assigns a high similarity because both messages
contain overlapping terms such as "twice" and "Spotify".

However, the underlying meanings are different:

- Query: duplicate billing/payment
- Retrieved case: unrelated content involving the word "twice"

### Why this matters

This is an important limitation of lexical retrieval.

A high cosine similarity score does not guarantee semantic relevance.

### Mitigation

NIA uses a minimum similarity threshold and evaluates retrieval separately
from response generation. However, the evaluation demonstrates that
thresholding alone cannot eliminate every semantic false positive.

A stronger production implementation could use:

- Sentence embeddings
- A cross-encoder reranker
- Intent-aware retrieval
- Metadata filtering
- Hybrid lexical + semantic search

---

## 6. Retrieval False Negatives

Several relevant queries did not retrieve sufficiently similar historical
evidence at the `0.6` threshold.

Examples:

- "My Spotify Premium subscription is not working"
- "I cannot play songs on Spotify"
- "How do I create a Spotify family plan?"

### Why this happens

The historical dataset may not contain sufficiently similar wording for
these queries. TF-IDF also depends heavily on lexical overlap.

For example, a customer may describe a playback problem using different
words from the historical cases.

### Lesson

Retrieval recall is an important limitation of the current approach.

A system can be safe against unsupported answers while still failing to
find useful historical evidence.

---

# Grounding and Escalation

NIA is designed so that the assistant does not blindly generate a response
when sufficient evidence is unavailable.

The agent checks:

1. Intent classification confidence
2. Whether historical evidence exists
3. Historical similarity threshold

If these checks fail, the request is escalated instead of returning an
unsupported historical response.

This creates a deliberate trade-off:

> Prefer escalation over an ungrounded customer-support answer.

---

# Evaluation Limitations

The evaluation sets are intentionally small and manually constructed.

The 200-example golden set is useful for comparing approaches, but it is
not large enough to establish production-level intent classification
performance.

The retrieval evaluation contains 12 targeted test cases and is therefore
best interpreted as a diagnostic evaluation rather than a statistically
representative benchmark.

Similarly, the agent-quality evaluation measures grounding and escalation
decisions against predefined expected outcomes. It does not constitute a
full human evaluation of response helpfulness.

---

# Key Takeaways

The evaluation demonstrates several important properties of NIA:

- Intent classification is measurable rather than assumed to work.
- Retrieval can be evaluated independently from classification.
- Historical evidence can ground responses.
- Unsupported requests can be escalated.
- Lexical retrieval can produce misleading high-similarity matches.
- Short and multi-intent customer messages remain difficult.
- Better semantic retrieval and reranking are natural next improvements.

The system therefore prioritizes **measurability, grounding, and
transparent failure analysis** rather than presenting the prototype as a
fully production-ready support system.
