"""
Pydantic schema for validating the final reimbursement decision.
Ensures the LLM always returns a structured and consistent response format.
"""

from pydantic import BaseModel
from typing import List, Optional

class DecisionOutput(BaseModel):
    decision:str
    approved_amount: Optional[float] = None
    rejected_amount: Optional[float] = None
    missing_documents:List[str]
    policy_reference:List[str]
    confidence:float
    explanation:str
    


