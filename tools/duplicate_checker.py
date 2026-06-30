"""
Duplicate claim detection tool.
Prevents reimbursement for the same trip being submitted multiple times.

"""

def duplicate_checker(claim, all_claims):

    trip_id = claim["trip_id"]

    count = 0

    for existing_claim in all_claims:

        if existing_claim["trip_id"] == trip_id:
            count += 1

    if count > 1:

        return {
            "status": "FAIL",
            "reason": "Duplicate claim detected"
        }

    return {
        "status": "PASS",
        "reason": "No duplicate found"
    }