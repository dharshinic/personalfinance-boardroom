import json
import requests
import streamlit as st

st.set_page_config(page_title="PersonalFinance Boardroom", page_icon="💼", layout="wide")

NEURO_SAN_URL = "http://localhost:8080/api/v1/boardroom/streaming_chat"

# ---------- Sidebar: Financial Intake Form (builds sly_data) ----------
st.sidebar.header("Your Financial Snapshot")
st.sidebar.caption("This data stays out of the AI's raw prompt (sly-data) -- only derived numbers are used by tools.")

monthly_income = st.sidebar.number_input("Monthly income ($)", min_value=0, value=5000, step=100)

st.sidebar.subheader("Monthly Expenses")
housing = st.sidebar.number_input("Housing", min_value=0, value=1500, step=50)
food = st.sidebar.number_input("Food", min_value=0, value=500, step=50)
transportation = st.sidebar.number_input("Transportation", min_value=0, value=300, step=50)
entertainment = st.sidebar.number_input("Entertainment", min_value=0, value=200, step=50)
other_expenses = st.sidebar.number_input("Other", min_value=0, value=400, step=50)

savings_balance = st.sidebar.number_input("Savings balance ($)", min_value=0, value=3000, step=100)
retirement_balance = st.sidebar.number_input("Retirement balance ($)", min_value=0, value=12000, step=500)
age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=29)

st.sidebar.subheader("Debts")
num_debts = st.sidebar.number_input("Number of debts", min_value=0, max_value=5, value=2)
debts = []
for i in range(num_debts):
    st.sidebar.markdown(f"**Debt {i+1}**")
    name = st.sidebar.text_input(f"Name {i+1}", value=f"Debt {i+1}", key=f"debt_name_{i}")
    balance = st.sidebar.number_input(f"Balance {i+1} ($)", min_value=0, value=5000, step=100, key=f"debt_balance_{i}")
    apr = st.sidebar.number_input(f"APR {i+1} (%)", min_value=0.0, value=15.0, step=0.5, key=f"debt_apr_{i}") / 100
    min_payment = st.sidebar.number_input(f"Min payment {i+1} ($)", min_value=0, value=100, step=10, key=f"debt_min_{i}")
    debts.append({"name": name, "balance": balance, "apr": apr, "min_payment": min_payment})

st.sidebar.subheader("Risk Tolerance Survey")
comfort = st.sidebar.slider("Comfort with market drops (1-5)", 1, 5, 3)
horizon = st.sidebar.number_input("Investment horizon (years)", min_value=0, value=30, step=1)
stability = st.sidebar.slider("Income stability (1-5)", 1, 5, 4)

sly_data = {
    "monthly_income": monthly_income,
    "monthly_expenses": {
        "housing": housing, "food": food, "transportation": transportation,
        "entertainment": entertainment, "other": other_expenses
    },
    "savings_balance": savings_balance,
    "debts": debts,
    "age": age,
    "retirement_balance": retirement_balance,
    "risk_survey_answers": {
        "comfort_with_market_drops": comfort,
        "investment_horizon_years": horizon,
        "income_stability": stability
    }
}

# ---------- Main: Chat ----------
st.title("💼 Personal Finance Boardroom")
st.caption("Ask a financial question. The Boardroom Chair will consult relevant specialist advisors and synthesize a recommendation.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_trace" not in st.session_state:
    st.session_state.last_trace = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask the Boardroom a financial question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("The Boardroom is deliberating..."):
            try:
                payload = {
                    "user_message": {"type": "HUMAN", "text": user_input},
                    "sly_data": sly_data
                }
                response = requests.post(NEURO_SAN_URL, json=payload, stream=True, timeout=120)

                final_text = ""
                trace = []

                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                    except json.JSONDecodeError:
                        continue

                    trace.append(chunk)

                    # Try common shapes for the final assistant text.
                    text_candidate = None
                    if isinstance(chunk, dict):
                        if "response" in chunk and isinstance(chunk["response"], dict):
                            text_candidate = chunk["response"].get("text")
                        elif "chat_message" in chunk and isinstance(chunk["chat_message"], dict):
                            text_candidate = chunk["chat_message"].get("text")
                        elif "text" in chunk:
                            text_candidate = chunk.get("text")

                    if text_candidate:
                        final_text = text_candidate

                if not final_text:
                    final_text = "(No text found in response -- check the reasoning trace below and share it so we can fix the parsing.)"

                st.write(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
                st.session_state.last_trace = trace

            except Exception as e:
                st.error(f"Error contacting the Boardroom: {e}")

if st.session_state.last_trace:
    with st.expander("🔍 Reasoning Trace (agent delegation log)"):
        st.json(st.session_state.last_trace)