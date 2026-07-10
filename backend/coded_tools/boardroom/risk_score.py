from typing import Any, Dict
from neuro_san.interfaces.coded_tool import CodedTool


class RiskScoreTool(CodedTool):
    """
    Computes a simple risk tolerance category from sly_data survey answers.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        answers = sly_data.get("risk_survey_answers", {})

        comfort = answers.get("comfort_with_market_drops", 3)
        horizon = answers.get("investment_horizon_years", 10)
        stability = answers.get("income_stability", 3)

        score = comfort + stability + min(horizon / 10, 3)

        if score >= 8:
            category = "aggressive"
        elif score >= 5:
            category = "moderate"
        else:
            category = "conservative"

        return {
            "risk_category": category,
            "justification": f"Based on comfort={comfort}, horizon={horizon}yrs, income stability={stability}"
        }