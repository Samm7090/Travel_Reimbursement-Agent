"""
Receipt validation tool.

Business Rule:
- Any expense above $25 requires a receipt.
- Missing receipts should trigger Manual Review.

This tool checks whether required documents have been attached to the reimbursement claim.
"""
def receipt_checker(claim:dict) -> dict:

    if claim["receipt_attached"]:

        return {
            "status": "PASS",
            "missing_documents": []
        }

    return {
        "status": "FAIL",
        "missing_documents": ["Receipt Missing"]
    }