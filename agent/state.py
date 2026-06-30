"""
This state object is passed between nodes, it act as InputSchema for all the nodes:
- Input claim details
- Retrieved policy context
- Tool execution results
- Final reimbursement decision
- Audit logs for explainability
"""

from typing import TypedDict

class AgentState(TypedDict):
    claim: dict
    policy_context:str
    tool_result:dict
    decision:dict
    audit_log:list


