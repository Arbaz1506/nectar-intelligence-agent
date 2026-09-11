# NIA - Nectar Intelligence Assistant

NIA is a lightweight, measurable customer-support intelligence agent built
around historical SpotifyCares conversations from the Kaggle Customer Support
on Twitter (TWCS) dataset.

NIA is designed for support workflows rather than open-ended conversation. It
classifies each message, retrieves similar historical cases, returns a response
only when the evidence is strong enough, and escalates unsupported requests.

## What It Does

Given a customer message, NIA:

1. Predicts one of 10 support intents and a confidence score.
2. Searches historical customer messages with TF-IDF and cosine similarity.
3. Uses the best matching historical reply as grounded evidence.
4. Escalates when the intent or retrieved evidence is not reliable enough.
5. Returns structured metadata for inspection and evaluation.

The intent labels are:

| Intent | Scope |
| --- | --- |
| `premium_subscription` | Premium plans, upgrades, cancellations, and access |
| `student_plan` | Student discounts and student subscriptions |
| `family_plan` | Family plans and family subscriptions |
| `billing_payment` | Charges, refunds, invoices, and payment failures |
| `account_login_security` | Login, password, access, and account security |
| `app_technical_issue` | App crashes, bugs, freezes, loading, and updates |
| `playback_music_issue` | Music playback, pauses, skips, and listening problems |
| `playlist_library` | Playlists, liked songs, saved music, and library issues |
| `feature_information` | Questions about Spotify features and functionality |
| `feedback_other` | General feedback and out-of-scope messages |

## Repository Layout

```text
src/
       agent.py              Intent classification and end-to-end agent workflow
       retrieval.py          TF-IDF historical-case retrieval
       historical_cases.py   TWCS customer/support pair construction
       preprocessing.py      Text and dataset preprocessing helpers
demo.py                 Interactive command-line demo
data/raw/archive/       Source TWCS data
evaluation/             Golden set, evaluation scripts, tests, and results
```

## Setup

Use Python 3.10 or newer, then install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install packages:

```bash
python -m pip install -r requirements.txt
```

The repository includes the prepared SpotifyCares historical cases used by the
agent. The original TWCS files are kept under `data/raw/archive/`.

## Run the Demo

From the repository root:

```bash
python demo.py
```

Enter a Spotify support message at the prompt. Type `exit` to quit. The demo
prints the predicted intent, confidence, retrieval similarity, grounding state,
escalation state, response, and retrieved evidence.

Example messages:

```text
My Spotify app keeps crashing after the update.
I was charged twice for Spotify Premium.
How do I make pancakes?
```

The final example should demonstrate the escalation path because it is outside
the available Spotify support evidence.

## Evaluation

Run evaluation scripts from the repository root. They write their results back
to the `evaluation/` directory.

```bash
python evaluation/evaluate_agent.py
python evaluation/evaluate_retrieval.py
python evaluation/evaluate_agent_quality.py
```

The repository also contains focused executable checks:

```bash
python evaluation/test_agent.py
python evaluation/test_historical_cases.py
python evaluation/test_retrieval.py
```

Important evaluation artifacts include:

- `evaluation/golden_set.csv`: labeled intent evaluation examples
- `evaluation/historical_cases.csv`: reconstructed SpotifyCares cases
- `evaluation/agent_intent_results.csv`: intent predictions and labels
- `evaluation/agent_quality_results.csv`: response-quality results
- `evaluation/retrieval_results.csv`: retrieval evaluation results
- `evaluation/failure_analysis.md`: documented failure patterns

## Architecture

```text
Customer message
       |
       v
Intent classifier -> intent + confidence
       |
       v
TF-IDF historical retriever -> similar cases + similarity
       |
       +--> sufficient evidence -> historical, grounded reply
       |
       +--> insufficient evidence -> escalation
```

Intent classification is implemented with a transparent keyword and scoring
approach. Retrieval uses a TF-IDF vectorizer with English stop-word removal and
unigrams/bigrams, followed by cosine similarity. This keeps the prototype
lightweight, inspectable, and easy to evaluate.

## Dataset Notes

The project uses the SpotifyCares subset of the Kaggle TWCS dataset. Historical
customer/support pairs are reconstructed through the
`in_response_to_tweet_id` relationship. The prepared dataset contains more than
43,000 historical cases.

The dataset is used for experimentation and evaluation. It may contain noisy,
duplicated, abbreviated, or context-dependent social-media conversations, so a
retrieved reply should be treated as supporting evidence rather than a guarantee
that the response is correct for every current customer situation.

## Limitations

- The intent classifier is rule-based and may struggle with ambiguous wording.
- TF-IDF retrieval does not understand meaning beyond word overlap.
- The prototype has no live Spotify account, billing, or product integration.
- Historical responses can be incomplete or outdated.
- Escalation thresholds are heuristic and should be tuned with production data.

For these reasons, NIA is best viewed as an evidence-aware support-assistance
prototype, not an autonomous production support system.
