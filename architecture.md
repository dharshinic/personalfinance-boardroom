# Architecture: Personal Finance Boardroom

## What this project does
Personal Finance Boardroom lets a user describe a financial question or
situation and receive a synthesized recommendation from a "board" of
specialist AI advisors (Budgeting, Investment, Tax, Debt), coordinated
by a Boardroom Chair agent. Rather than one generic AI giving one
generic answer, this system models how real financial decisions
involve multiple expert perspectives that sometimes disagree -- and
makes those trade-offs explicit to the user.

## How it achieves that: Agentic System Design

This project is built entirely on **Neuro SAN**, using its declarative,
data-driven multi-agent orchestration.

### Agent Network (see `backend/registries/boardroom.hocon`)
- **boardroom_chair**: front-man agent. Receives the user's question and
  decides, using its own judgment (not hardcoded rules), which
  specialists are relevant to consult.
- **budgeting_advisor**, **investment_advisor**, **tax_advisor**,
  **debt_advisor**: specialist agents, each with domain-specific
  instructions and their own CodedTool.
- **risk_profiler**: a shared sub-agent. Both `investment_advisor` and
  `debt_advisor` can independently choose to call it -- this
  demonstrates Neuro SAN's **AAOSA (Adaptive Agent Oriented Software
  Architecture) protocol**: decentralized delegation where agents
  decide amongst themselves who to involve, rather than following a
  fixed pipeline.

### Sly-Data (privacy-preserving data flow)
All sensitive financial figures (income, expenses, debt balances, APRs,
retirement savings) are passed as **sly_data**, a Neuro SAN mechanism
that keeps this information out of the LLM's raw prompt entirely.
CodedTools read sly_data directly in Python and return only derived,
safe values (e.g., "debt-to-income ratio: 38%, high" instead of raw
account balances) back to the agents. This means the underlying
numbers are never seen or logged by the LLM provider.

### CodedTools (see `backend/coded_tools/boardroom/`)
- `BudgetCalculatorTool`: computes savings rate and expense breakdown
- `DebtPayoffTool`: compares avalanche vs. snowball payoff strategies
- `TaxEstimatorTool`: estimates tax owed using static 2026 bracket data
- `RiskScoreTool`: computes a risk-tolerance category from survey answers

These are pure, deterministic Python -- no LLM calls -- demonstrating
Neuro SAN's intended split between natural-language reasoning (agents)
and deterministic computation (tools).

### LLM Configuration
Configured via Neuro SAN's provider-agnostic `llm_config`, currently
using Google Gemini (`gemini-2.5-flash`). Per-agent LLM overrides are
supported natively by the framework, letting different agents use
different models based on the reasoning complexity they need.

### Frontend
A Streamlit app (`frontend/streamlit_app.py`) provides:
- A structured intake form that builds the sly_data payload
- A chat interface to the agent network
- A reasoning-trace viewer, exposing which agents/tools were invoked
  and in what order -- making the AAOSA delegation visible to the user

## Why this is a genuine multi-agent system (not a single LLM call)
No single prompt could reliably hold "budgeting logic + debt strategy
math + tax bracket data + risk profiling + trade-off synthesis" without
either hallucinating numbers or losing coherence. By splitting these
into specialist agents with dedicated tools, each piece of reasoning is
grounded in real computation, and the Chair's synthesis step explicitly
surfaces disagreements between specialists that a single-agent system
would likely paper over.