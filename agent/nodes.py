"""
LangGraph nodes used in the reimbursement workflow.
"""

from rag.retriever import retrieve_policy

from tools.receipt_checker import receipt_checker
from tools.limit_checker import limit_checker
from tools.approval_checker import approval_checker

from agent.llm import llm_with_tools

#------Node-1 Retrieve Policy---------
def retreieve_policy(state):
    
    claim=state["claim"]

    categories=[]
    for category in ["stay","food","travel"]:
        if claim.get(category,0)>0:
            categories.append(category)

    query=(" ".join(categories)+" reimbursement policy")

    policy_context=retrieve_policy(query)

    state["policy_context"]=policy_context

    state["audit_log"].append(f"Policy Retrieved using query:{query}")

    return state


#------Node-2 Decision Node---------
from langchain_core.messages import HumanMessage
from agent.llm import llm_with_tools
import json

def decision_node(state):
    if not state["messages"]:
        prompt = f"""
    You are an automated Travel Reimbursement Approval Agent.
    Your job is to evaluate the reimbursement claim provided below.
    
    DO NOT ask the user for additional information.
    DO NOT request expense amounts.
    DO NOT request receipt status.
    DO NOT request approval status.

    Use the claim below as the source of truth.
    Policy:{state["policy_context"]}
    Claim:{json.dumps(state["claim"], indent=2)}

   Before producing a final answer you MUST call all three tools.

    Required tool sequence:

    1. receipt_checker(receipt_attached)
    2. limit_checker(stay, food, travel)
    3. approval_checker(stay, food, travel, manager_approval, director_approval)

    Do not answer until all three tool results have been received.

    Do not skip any check.

    Do not ask the user for additional information.

    After all tool checks are completed, return a final decision.

    Possible decisions:
    - APPROVED
    - PARTIALLY_APPROVED
    - REJECTED
    - MANUAL_REVIEW
    """
    
        messages = [HumanMessage(content=prompt)]

    # print(prompt)
    else:
        messages=state["messages"]

    response = llm_with_tools.invoke(messages)
    
    # print("\nTOOL CALLS:")
    # print(response.tool_calls)

    # print("\nCONTENT:")
    # print(response.content)

    # print("\nFULL RESPONSE:")
    # print(response)

    return {
        "messages": [response],
        "audit_log": state["audit_log"] + ["Agent executed"]
    }

#----------Node 3: Output Node--------
from models.output_schema import DecisionOutput

def output_node(state):

    final_message = state["messages"][-1].content

    if "approved" in final_message.lower():
        decision = "APPROVED"
    elif "rejected" in final_message.lower():
        decision = "REJECTED"
    else:
        decision = "MANUAL_REVIEW"

    result = DecisionOutput(
        decision="decision",
        approved_amount=0,
        rejected_amount=0,
        missing_documents=[],
        policy_reference=[],
        confidence=0.80,
        explanation=final_message
    )

    state["decision"] = result.model_dump()
    
    print("\nFINAL MESSAGE OBJECT")
    print(state["messages"][-1])

    print("\nFINAL CONTENT")
    print(state["messages"][-1].content)

    state["audit_log"].append("Structured output generated")

    return state