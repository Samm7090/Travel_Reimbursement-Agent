"""
Pydantic schema for validating the final reimbursement decision.
Ensures the LLM always returns a structured and consistent response format.
"""

from pydantic import BaseModel
from typing import List

class DecisionOutput(BaseModel):
    decision:str
    approved_amount:float
    rejected_amount:float
    missing_documents:List[str]
    policy_reference:List[str]
    confidence:float
    explanation:str
    
