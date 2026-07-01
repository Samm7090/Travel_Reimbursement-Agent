"""
This state object is passed between nodes, it act as InputSchema for all the nodes:
- Input claim details
- Retrieved policy context
- Tool execution results
- Final reimbursement decision
- Audit logs for explainability
"""

from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    claim: dict
    messages: Annotated[list[BaseMessage],add_messages]
    policy_context:str
    decision:dict
    audit_log:list[str]


