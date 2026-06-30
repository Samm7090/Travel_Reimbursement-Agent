"""
Pydantic schema for validating the final reimbursement decision.
Ensures the LLM always returns a structured and consistent response format.
"""

from pydantic import BaseModel

class DecisionOutput(BaseModel):
    decision:str
    approved_amount:float
    rejected_amount:float
    missing_documents:list
    policy_reference:list
    confidience:float
    explanation:str
    audit_log:list
    
