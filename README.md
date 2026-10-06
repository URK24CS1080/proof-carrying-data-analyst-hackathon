\# Proof-Carrying Data Analyst



\## HackNex PS8 — HNX26PSI08



An AI-powered data analyst that provides not only an answer, but also executable proof that the answer is correct.



> \*\*AI proposes. Local system proves.\*\*



\## Problem



Traditional AI data analysis systems can produce confident answers without providing reliable evidence that the result is actually correct.



Our system addresses this by separating:



\- AI-based question understanding and planning

\- Local data execution

\- Executable proof generation

\- Independent verification



A confident wrong answer is worse than a correct refusal.



\## Core Flow



```text

User Question

&#x20;     ↓

LLM Planner

&#x20;     ↓

Validated JSON Plan

&#x20;     ↓

Local Executor

&#x20;     ↓

Result + Proof Code

&#x20;     ↓

Verifier

&#x20;     ↓

Verified Answer / Refusal / Clarification

&#x20;     ↓

Streamlit UI

