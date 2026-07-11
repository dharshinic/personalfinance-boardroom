

# Personal Finance Boardroom

An AI-powered "board of financial experts" that reviews your budgeting, tax, debt, and investment questions and returns one synthesized recommendation -- surfacing where the specialists agree and where they disagree. Built with Cognizant's [neuro-san](https://github.com/cognizant-ai-lab/neuro-san) multi-agent framework.

---

## Prerequisites

- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/apikey) (free tier) -- the agents use `gemini-flash-lite-latest`
- A working [neuro-san-studio](https://github.com/cognizant-ai-lab/neuro-san-studio) installation (this project reuses its virtual environment; see Setup below)

---

## Setup

### 1. Clone the repository
```
git clone https://github.com/dharshinic/personalfinance-boardroom.git
cd personalfinance-boardroom
```

### 2. Create and activate a virtual environment

If you already have a working neuro-san-studio virtual environment, you can reuse it instead of creating a new one:
Windows
```
neuro-san-studio\venv\Scripts\activate
```
macOS / Linux
```
source neuro-san-studio/venv/bin/activate
```
Otherwise, create a fresh one:
```
python -m venv venv
```
Windows
```
venv\Scripts\activate
```
macOS / Linux
```
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set your environment variables

This project needs four environment variables set before starting the backend. Windows (cmd) example:
```
set GOOGLE_API_KEY=your-gemini-api-key-here
set AGENT_MANIFEST_FILE=FULL_PATH_TO_REPO\backend\registries\manifest.hocon
set AGENT_TOOL_PATH=FULL_PATH_TO_REPO\backend\coded_tools
set PYTHONPATH=FULL_PATH_TO_REPO
```

macOS / Linux equivalent uses `export` instead of `set`.

For convenience, two Windows startup scripts are included as templates -- copy them, fill in your own paths and key, and they are excluded from version control via `.gitignore` so your key is never committed:
- `start_server.bat` -- starts the neuro-san backend
- `start_nsflow.bat` -- starts the optional nsflow visual debugger (not required to run the app)

---

## Running the App

### Launch the backend (neuro-san server)
```
python -m neuro_san.service.main_loop.server_main_loop
```

Leave this running in its own terminal. It serves the agent network over HTTP on port `8080`.

### Launch the Streamlit web interface

In a separate terminal (with the same environment variables set, minus `AGENT_TOOL_PATH`/`AGENT_MANIFEST_FILE` which are backend-only):
```
streamlit run frontend/streamlit_app.py
```

Open the URL printed in the terminal (usually `http://localhost:8501`).

**Example prompts:**
- `I have $5,000 in credit card debt at 22% APR and $3,000 in savings. Should I invest or pay off debt first?`
- `What tax bracket am I in?`
- `How should I budget my income?`

Fill in the sidebar "Your Financial Snapshot" form first -- it builds the private financial data (sly-data) the specialists use to ground their answers in real numbers.

### Optional: visual agent graph (nsflow)
```
python -m nsflow.run --client_only
```

Open `http://localhost:4173/home`, connect to `localhost:8080`, and select the `boardroom` network to see the live multi-agent delegation graph. This is a development/demo tool only -- the Streamlit app does not depend on it.

---

## Project Structure

```
personalfinance-boardroom/
├── backend/
│   ├── registries/
│   │   ├── manifest.hocon           # Active agent registry
│   │   └── boardroom.hocon          # Multi-agent network definition
│   └── coded_tools/
│       └── boardroom/
│           ├── budget_calculator.py  # CodedTool: budget breakdown & savings rate
│           ├── debt_payoff.py        # CodedTool: avalanche vs snowball payoff
│           ├── tax_estimator.py      # CodedTool: 2026 tax bracket estimation
│           ├── risk_score.py         # CodedTool: risk tolerance scoring
│           └── data/
│               └── tax_brackets_2026.json
├── frontend/
│   └── streamlit_app.py             # Streamlit chat UI + financial intake form
├── requirements.txt                 # Python dependencies
├── architecture.md                  # System architecture
├── summary.md                       # Project summary
└── README.md                        # This file
```


## How It Works

The backend is a **multi-agent system** built with neuro-san:

| Agent | Role |
|---|---|
| `boardroom_chair` | Orchestrator -- decides which specialists a question needs, then synthesizes their input into one recommendation |
| `budgeting_advisor` | Analyzes spending patterns and savings rate via `BudgetCalculatorTool` |
| `investment_advisor` | Gives investment guidance, consulting `risk_profiler` when risk tolerance matters |
| `tax_advisor` | Estimates tax bracket and rates via `TaxEstimatorTool` |
| `debt_advisor` | Compares debt payoff strategies via `DebtPayoffTool`, also consults `risk_profiler` |
| `risk_profiler` | Shared sub-agent computing risk tolerance via `RiskScoreTool` -- callable independently by both `investment_advisor` and `debt_advisor`, demonstrating neuro-san's AAOSA decentralized delegation |

All financial figures (income, debts, balances) are passed as neuro-san **sly-data** -- never entering the LLM's raw prompt -- and read directly by the CodedTools, which return only derived, safe values to the agents.

See [architecture.md](architecture.md) and [summary.md](summary.md) for a detailed description.

---

## Dependencies

| Package | Purpose |
|---|---|
| neuro-san | Multi-agent orchestration framework |
| streamlit | Web chat interface |
| requests | HTTP client for frontend-backend communication |
| langchain-google-genai | Gemini LLM provider integration |

See `requirements.txt` for exact pinned versions.

---

## Troubleshooting

**`GOOGLE_API_KEY` not found / auth errors** -- Confirm you ran `set GOOGLE_API_KEY=...` in the *same terminal* used to start the backend server; environment variables do not persist across terminals.

**`No reasonable agent tool path found in PYTHONPATH`** -- `AGENT_TOOL_PATH` was not set (or not set in this terminal) before starting the server. Re-run the full environment variable block above.

**`No fully-specified LLM found` / model 404 errors** -- Google periodically deprecates specific Gemini model versions for new API keys. Run `curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_KEY"` to see which models your key can currently access, and update `model` in `backend/registries/boardroom.hocon` accordingly. The `-latest` alias models (e.g. `gemini-flash-lite-latest`) are the most resilient to this.

**`429 RESOURCE_EXHAUSTED` (quota exceeded)** -- The Gemini free tier limits requests per day per model. Wait for the daily reset, switch to a different model tier (e.g. Flash-Lite instead of Flash), or use a different API key.

**Streamlit shows a connection error** -- The backend server (`python -m neuro_san.service.main_loop.server_main_loop`) must be running in a separate terminal before starting Streamlit.

**Port already in use** -- Pass a different port: `streamlit run frontend/streamlit_app.py --server.port 8502`
'@ | Set-Content -Encoding utf8 README.md
