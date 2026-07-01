"""
Approval hierarchy validation tool.

Business Rules:
- Claims > $500 require manager approval.
- Claims > $1000 require director approval.

This tool verifies whether the necessary approvals have been attached.
"""
from langchain.tools import tool
import json


with open("data/approval_matrix.json", "r") as f:
    APPROVAL_RULES = json.load(f)

@tool
def approval_checker(stay: float, food: float, travel: float, manager_approval: bool,director_approval: bool):
    """
    Checks whether required approvals are present.
    """
    
    total_amount = stay + food + travel
    manager_limit = APPROVAL_RULES["manager_threshold"]
    director_limit = APPROVAL_RULES["director_threshold"]

    if total_amount > director_limit:

        if not director_approval:
            result_d={
                "status": "FAIL",
                "reason": "Director approval required"
            }

            print(result_d)
            return result_d

    elif total_amount > manager_limit:

        if not manager_approval:
            result_m={
                "status": "FAIL",
                "reason": "Manager approval required"
            }

            print(result_m)
            return result_m

    result_p={
        "status": "PASS",
        "reason": "Approval requirements satisfied"
    }

    print(result_p)
    return result_p