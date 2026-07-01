"""
Receipt validation tool.

Business Rule:
- Any expense above $25 requires a receipt.
- Missing receipts should trigger Manual Review.

This tool checks whether required documents have been attached to the reimbursement claim.
"""
from langchain.tools import tool

@tool
def receipt_checker(receipt_attached: bool):
    """
    Checks whether a receipt is attached.
    """
     
    if receipt_attached:
        
        result_p={
            "status": "PASS",
            "missing_documents": []
        } 
        
        print(result_p)
        return result_p 

    result_f={
        "status": "FAIL",
        "missing_documents": ["Receipt Missing"]
    }

    print(result_f)
    return result_f