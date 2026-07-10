from typing import Any, Dict
from neuro_san.interfaces.coded_tool import CodedTool


class BudgetCalculatorTool(CodedTool):
    """
    Reads income/expenses from sly_data and returns a category breakdown
    and savings rate. Never returns raw account numbers beyond what's
    needed for the advisor's reasoning.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        income = sly_data.get("monthly_income", 0)
        expenses = sly_data.get("monthly_expenses", {})

        total_expenses = sum(expenses.values())
        savings_rate = 0.0
        if income > 0:
            savings_rate = round((income - total_expenses) / income * 100, 1)

        breakdown = {}
        for category, amount in expenses.items():
            pct = round((amount / income * 100), 1) if income > 0 else 0
            breakdown[category] = f"{pct}% of income"

        return {
            "savings_rate_percent": savings_rate,
            "category_breakdown": breakdown,
            "total_monthly_expenses": total_expenses,
            "flag": "healthy" if savings_rate >= 15 else "tight" if savings_rate >= 0 else "overspending"
        }