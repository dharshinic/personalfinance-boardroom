# Project Summary: Personal Finance Boardroom

## Problem
Most people get financial advice from a single source at a time --
a budgeting app, a robo-advisor, a tax calculator -- each blind to the
others. Real financial decisions (e.g., "pay off debt or invest?")
require weighing competing expert perspectives simultaneously, which is
exactly what a human financial advisory board would do, but that level
of service isn't accessible to most people.

## Solution
Personal Finance Boardroom simulates a board of specialist financial
advisors -- Budgeting, Investment, Tax, and Debt -- coordinated by a
Chair agent, built entirely on the Neuro SAN multi-agent orchestration
framework. Users describe their situation once; the system determines
which specialists are relevant, consults them (with real computation
via CodedTools, not hallucinated numbers), and returns one synthesized
recommendation that explicitly names where advisors agreed or
disagreed.

## Target Users
Individuals seeking a second opinion on personal financial decisions
who don't have access to (or can't afford) a real financial advisory
team, and want more transparency than a single-answer chatbot provides.

## How Neuro SAN Powers This
- **HOCON-declarative agent network**: the entire board (Chair + 4
  specialists + shared Risk Profiler) is defined in one data file, no
  hardcoded orchestration logic.
- **AAOSA adaptive delegation**: the Chair decides which specialists to
  consult per-question; two specialists (Investment and Debt) can
  independently call a shared Risk Profiler sub-agent -- demonstrating
  decentralized, non-pipeline delegation.
- **Sly-Data**: all real financial figures are passed to CodedTools
  without ever entering the LLM's prompt, addressing a genuine privacy
  concern in financial applications.
- **CodedTools**: deterministic Python handles all actual math (budget
  ratios, debt payoff ordering, tax brackets, risk scoring) -- agents
  reason in natural language, tools compute.
- **Provider-agnostic LLM config**: currently running on Google Gemini,
  demonstrating Neuro SAN's LLM-agnosticism.

## Key Features
- Structured financial intake form (Streamlit)
- Adaptive multi-agent consultation (not a fixed pipeline)
- Real, tool-grounded financial calculations
- Transparent reasoning trace showing agent/tool delegation
- Explicit surfacing of advisor disagreement and trade-offs

## Novelty
Unlike Neuro SAN's official example use-cases (insurance, banking,
telco, airline), this project targets an underserved personal-finance
"board of experts" pattern, chosen specifically to showcase AAOSA's
decentralized delegation (via the shared Risk Profiler) in a way that's
visually and narratively compelling in a live demo.

## Business Potential
This pattern generalizes to any domain where multiple expert
perspectives with occasional disagreement produce better decisions than
a single generalist answer -- e.g., legal, healthcare triage, or HR
policy questions -- making the underlying architecture reusable well
beyond personal finance.