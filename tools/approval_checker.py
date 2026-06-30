"""
Approval hierarchy validation tool.

Business Rules:
- Claims > $500 require manager approval.
- Claims > $1000 require director approval.

This tool verifies whether the necessary approvals have been attached.
"""

import json


with open("data/approval_matrix.json", "r") as f:
    APPROVAL_RULES = json.load(f)


def approval_checker(total_amount: float, claim: dict) -> dict:

    manager_limit = APPROVAL_RULES["manager_threshold"]
    director_limit = APPROVAL_RULES["director_threshold"]

    if total_amount > director_limit:

        if not claim.get("director_approval", False):
            return {
                "status": "FAIL",
                "reason": "Director approval required"
            }

    elif total_amount > manager_limit:

        if not claim.get("manager_approval", False):
            return {
                "status": "FAIL",
                "reason": "Manager approval required"
            }

    return {
        "status": "PASS",
        "reason": "Approval requirements satisfied"
    }