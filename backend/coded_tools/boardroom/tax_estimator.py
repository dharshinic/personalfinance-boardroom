import json
import os
from typing import Any, Dict
from neuro_san.interfaces.coded_tool import CodedTool


class TaxEstimatorTool(CodedTool):
    """
    Estimates marginal and effective tax rate from annual income
    (derived from sly_data monthly_income) using static 2026 bracket data.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        annual_income = sly_data.get("monthly_income", 0) * 12

        data_path = os.path.join(os.path.dirname(__file__), "data", "tax_brackets_2026.json")
        with open(data_path, "r") as f:
            brackets = json.load(f)["single"]

        tax_owed = 0.0
        prev_cap = 0
        marginal_rate = 0.0

        for bracket in brackets:
            cap = bracket["up_to"] if bracket["up_to"] is not None else float("inf")
            if annual_income > prev_cap:
                taxable_in_bracket = min(annual_income, cap) - prev_cap
                tax_owed += taxable_in_bracket * bracket["rate"]
                marginal_rate = bracket["rate"]
            prev_cap = cap
            if annual_income <= cap:
                break

        effective_rate = round((tax_owed / annual_income) * 100, 2) if annual_income > 0 else 0

        return {
            "estimated_annual_tax": round(tax_owed, 2),
            "marginal_rate_percent": round(marginal_rate * 100, 1),
            "effective_rate_percent": effective_rate
        }