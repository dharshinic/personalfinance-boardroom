# Project Summary: Personal Finance Boardroom

## Problem

Most people get financial advice from a single source at a time — a budgeting app, a robo-advisor, a tax calculator — each blind to the others. Real financial decisions (e.g., "pay off debt or invest?") require weighing competing expert perspectives simultaneously: a debt advisor and an investment advisor can look at the same numbers and reasonably disagree. That's exactly what a human financial advisory board would do, but that level of service isn't accessible to most people, and a single generic chatbot tends to flatten that disagreement into one confident-sounding answer instead of surfacing it.

## Solution

Personal Finance Boardroom simulates a board of specialist financial advisors — Budgeting, Investment, Tax, and Debt — coordinated by a Chair agent, built entirely on the Neuro SAN multi-agent orchestration framework. Users describe their situation once; the system determines which specialists are relevant, consults them (with real computation via CodedTools, not hallucinated numbers), and returns one synthesized recommendation that explicitly names where advisors agreed or disagreed.

## Target Users

Individuals seeking a second opinion on personal financial decisions who don't have access to (or can't afford) a real financial advisory team, and want more transparency than a single-answer chatbot provides. Secondary audience: people who want to understand the reasoning behind a recommendation, not just the recommendation itself.

## Example Interaction

To make the architecture concrete, here is what actually happens end-to-end for one real query.

**User fills in the sidebar intake form:** income $6,000/mo, $5,000 credit card debt at 22% APR, $3,000 in savings, moderate risk tolerance survey answers.

**User asks:** *"I have $5,000 in credit card debt at 22% APR and $3,000 in savings. Should I invest or pay off debt first?"*

**What happens inside the agent network:**

1. `boardroom_chair` reads the question and decides — using its own judgment, not a hardcoded rule — that this requires both `debt_advisor` and `investment_advisor`, since the question is explicitly a debt-vs-invest trade-off.
2. `debt_advisor` calls `DebtPayoffTool` with the sly-data debt figures, and gets back a derived metric (e.g., avalanche payoff timeline and the effective 22% "guaranteed return" of paying it off) — never the raw balances passed back through the LLM.
3. `debt_advisor` also calls the shared `risk_profiler` sub-agent to check whether the user's risk tolerance changes the recommendation.
4. In parallel, `investment_advisor` independently calls the *same* `risk_profiler` sub-agent — this is the AAOSA decentralized delegation in action: two specialists reaching the same shared resource on their own initiative, with no fixed pipeline dictating that order.
5. `investment_advisor` reasons that with typical market returns well below 22%, guaranteed debt payoff usually wins mathematically, but flags that the answer would change if there were an employer 401(k) match being left on the table.
6. `boardroom_chair` synthesizes both specialist responses into one answer, explicitly stating: *both advisors agree paying off the debt first is mathematically favorable given the 22% rate, with the investment advisor's one caveat about employer-matched retirement contributions.*
7. The Streamlit reasoning-trace viewer shows the user exactly which agents and tools fired, in what order — so the "board meeting" is visible, not a black box.

This is the pattern the project is built to showcase: specialists reasoning independently, sometimes converging and sometimes flagging caveats, synthesized into one transparent answer.

## How Neuro SAN Powers This

- **HOCON-declarative agent network** — the entire board (Chair + 4 specialists + shared Risk Profiler) is defined in one data file, with no hardcoded orchestration logic.
- **AAOSA adaptive delegation** — the Chair decides which specialists to consult per-question; two specialists (Investment and Debt) can independently call a shared Risk Profiler sub-agent, demonstrating decentralized, non-pipeline delegation.
- **Sly-Data** — all real financial figures are passed to CodedTools without ever entering the LLM's prompt, addressing a genuine privacy concern in financial applications.
- **CodedTools** — deterministic Python handles all actual math (budget ratios, debt payoff ordering, tax brackets, risk scoring); agents reason in natural language, tools compute.
- **Provider-agnostic LLM config** — currently running on Google Gemini, demonstrating Neuro SAN's LLM-agnosticism and support for per-agent model overrides.

## Key Features

- Structured financial intake form (Streamlit) that builds the private sly-data payload
- Adaptive multi-agent consultation — not a fixed pipeline
- Real, tool-grounded financial calculations (no hallucinated numbers)
- Transparent reasoning trace showing agent/tool delegation order
- Explicit surfacing of advisor disagreement and trade-offs

## Novelty

Unlike Neuro SAN's official example use-cases (insurance, banking, telco, airline), this project targets an underserved personal-finance "board of experts" pattern, chosen specifically to showcase AAOSA's decentralized delegation — via the shared Risk Profiler being called independently by two different specialists — in a way that's visually and narratively compelling in a live demo. The disagreement-surfacing synthesis step is also a deliberate departure from the typical single-answer financial chatbot pattern.

## Limitations & Future Work

- Tax estimation currently uses static 2026 bracket data rather than a live tax API, so it doesn't account for state taxes, deductions, or filing-status nuance.
- The board currently supports four fixed specialist roles; a natural extension is letting the Chair dynamically spin up narrower specialists (e.g., a retirement-specific advisor) rather than only choosing among a fixed roster.
- No persistence layer for returning users — each session starts fresh, so there's no history of past recommendations to build on.
- Given more time, the next priority would be adding a "confidence" or "consensus strength" indicator alongside the synthesized answer, so users can see at a glance how strongly the specialists agreed.

## Business Potential

The core pattern — multiple expert agents reasoning independently over privacy-preserved data, with a chair agent surfacing disagreement rather than hiding it — generalizes well beyond personal finance to any domain where a single generalist answer is actually a bad idea: legal first-opinions, healthcare triage, or HR policy questions, for example. In the financial services space specifically, the sly-data pattern (real numbers never touching the LLM prompt) is a genuine differentiator for institutions evaluating AI advisory tools under compliance and data-privacy constraints, and the reasoning-trace UI doubles as an auditability feature that a regulated financial product would need anyway.