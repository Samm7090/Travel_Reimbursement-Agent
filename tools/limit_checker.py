"""
Expense limit validation tool.
Compares claimed amounts against reimbursement limits defined by company policy.
Categories:
- Stay
- Food
- Travel
Any amount above the policy limit is automatically deducted from the approved amount.
"""

import json

with open("data/limits.json") as f:
    LIMITS = json.load(f)


def limit_checker(claim):

    approved = 0
    rejected = 0

    violations = []

    for category in ["stay", "food", "travel"]:

        claimed_amount = claim.get(category, 0)

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