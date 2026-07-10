from typing import Any, Dict, List
from neuro_san.interfaces.coded_tool import CodedTool


class DebtPayoffTool(CodedTool):
    """
    Compares avalanche (highest APR first) vs snowball (smallest balance
    first) payoff strategies using sly_data debt list.
    """

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Dict[str, Any]:
        debts: List[Dict[str, Any]] = sly_data.get("debts", [])

        if not debts:
            return {"message": "No debts on file."}

        avalanche_order = sorted(debts, key=lambda d: d["apr"], reverse=True)
        snowball_order = sorted(debts, key=lambda d: d["balance"])

        total_balance = sum(d["balance"] for d in debts)
        weighted_apr = sum(d["balance"] * d["apr"] for d in debts) / total_balance if total_balance else 0

        return {
            "total_debt": total_balance,
            "weighted_average_apr_percent": round(weighted_apr * 100, 2),
            "avalanche_order": [d["name"] for d in avalanche_order],
            "snowball_order": [d["name"] for d in snowball_order],
            "recommendation": (
                "avalanche"
                if weighted_apr > 0.10
                else "snowball"
            )
        }