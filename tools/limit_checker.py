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
def limit_checker(stay: float = 0, food: float = 0, travel: float = 0):
    """
    Checks reimbursement limits and calculates approved and rejected amounts.
    """

    approved = 0
    rejected = 0

    violations = []

    expenses = {
        "stay": stay,
        "food": food,
        "travel": travel
    }

    for category,claimed_amount in expenses.items():

        allowed_limit = LIMITS[category]

        if claimed_amount > allowed_limit:

            approved += allowed_limit

            rejected += claimed_amount - allowed_limit

            violations.append(
                f"{category} exceeded by {claimed_amount-allowed_limit}"
            )

        else:

            approved += claimed_amount

    
    return {
        "approved_amount": approved,
        "rejected_amount": rejected,
        "violations": violations
    }