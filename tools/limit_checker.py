"""
Expense limit validation tool.
Compares claimed amounts against reimbursement limits defined by company policy.
Categories:
- Stay
- Food
- Travel
Any amount above the policy limit is automatically deducted from the approved amount.
"""
from langchain.tools import tool
import json

with open("data/limits.json") as f:
    LIMITS = json.load(f)

@tool
def limit_checker(stay: float, food: float, travel: float):
    """
    Checks reimbursement limits and calculates approved and rejected amounts.
    """
    
    def safe_float(x):
        try:
            return float(x)
        except:
            return 0.0
    
    approved = 0
    rejected = 0

    violations = []
    breakdown = {}

    expenses = {
        "stay": safe_float(stay),
        "food": safe_float(food),
        "travel": safe_float(travel)
    }

    for category,claimed_amount in expenses.items():

        allowed_limit = LIMITS.get(category,0)

        if claimed_amount > allowed_limit:

            approved += allowed_limit

            rejected += claimed_amount - allowed_limit

            violations.append({"category": category,
                              "claimed": claimed_amount,
                              "allowed": allowed_limit,
                              "exceeded_by": claimed_amount - allowed_limit
            })

            breakdown[category] = {
                "status": "exceeded",
                "approved": allowed_limit,
                "rejected": claimed_amount - allowed_limit
            }

        else:

            approved += claimed_amount
            breakdown[category] = {
                "status": "within_limit",
                "approved": claimed_amount,
                "rejected": 0
            } 

    
    return {
    "approved_amount": round(approved, 2),
    "rejected_amount": round(rejected, 2),
    "violations": violations,
    "breakdown": breakdown
    }