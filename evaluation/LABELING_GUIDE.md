# NIA Golden Set — Labeling Guide

## Purpose

This guide defines how customer-support messages are labelled for the
NIA evaluation dataset.

The goal is to measure how well NIA identifies the customer's primary
support intent and decides whether the case can be handled automatically.

## Intent Labels

### 1. premium_subscription
Premium subscription status, upgrades, downgrades, Premium availability,
or general Premium account problems.

### 2. family_plan
Spotify Family invitations, members, Family eligibility, address issues,
or Family subscription problems.

### 3. student_plan
Student discount, student verification, eligibility, or Student Premium
problems.

### 4. billing_payment
Unexpected charges, incorrect pricing, payment failures, refunds,
trials, or payment-method problems.

### 5. account_login_security
Login, password reset, account recovery, email changes, hacked or
compromised accounts, or access problems.

### 6. app_technical_issue
Application crashes, errors, installation/update problems, compatibility,
or technical failures.

### 7. playback_music_issue
Problems playing music, songs, albums, offline playback, or playback
interruptions.

### 8. playlist_library
Playlist creation, transfer, sorting, saved music, playlist display,
or library-management problems.

### 9. feature_information
Questions about Spotify features, functionality, availability, or
product behavior where the customer is primarily asking for information.

### 10. feedback_other
General feedback, praise, complaints, unclear requests, or cases that
do not clearly fit another category.

## Primary Intent Rule

Choose the customer's **primary support problem**.

If a message contains multiple problems, select the issue that would
require the most important support action.

## Ambiguous Messages

If there is not enough information to confidently determine the intent,
use:

`feedback_other`

Do not guess based on a single keyword.

For example, the word "account" alone does not necessarily mean
`account_login_security`.

## Conversation Context

When previous messages are available, use them to understand short
follow-ups such as:

- "DM sent"
- "I tried that"
- "Still doesn't work"
- "Thanks"
- "Yes, that's the problem"

These messages should not automatically be treated as
`feedback_other` when their conversation context reveals the underlying
issue.

## Escalation Label

Each evaluation example should also contain:

`should_escalate`

Use `true` when the case reasonably requires human intervention,
especially for:

- hacked or compromised accounts
- account-specific investigations
- disputed or unclear charges
- refund investigations
- cases requiring private account information
- situations where historical evidence is insufficient
- cases where an automated response could create significant customer harm

Use `false` when the issue can reasonably be answered using reliable
historical support information without account-specific investigation.

## Important Principle

The golden set represents an evaluation target, not necessarily the
only correct wording of a response.

For replies, evaluate whether the response is correct, grounded,
helpful, and appropriately cautious rather than requiring exact
word-for-word matching.
