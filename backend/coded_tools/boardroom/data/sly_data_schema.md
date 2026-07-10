# Sly-Data Schema for PersonalFinance Boardroom

This is the structure of sly_data passed alongside each chat session.
It NEVER appears in any LLM prompt directly -- only CodedTools read it,
and they return only derived/safe values back to the agents.

{
  "monthly_income": 5000,
  "monthly_expenses": {
    "housing": 1500,
    "food": 500,
    "transportation": 300,
    "entertainment": 200,
    "other": 400
  },
  "savings_balance": 3000,
  "debts": [
    {"name": "Credit Card", "balance": 5000, "apr": 0.22, "min_payment": 150},
    {"name": "Student Loan", "balance": 15000, "apr": 0.05, "min_payment": 200}
  ],
  "age": 29,
  "retirement_balance": 12000,
  "risk_survey_answers": {
    "comfort_with_market_drops": 3,
    "investment_horizon_years": 30,
    "income_stability": 4
  }
}