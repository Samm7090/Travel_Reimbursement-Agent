"""
LangGraph nodes used in the reimbursement workflow.
"""

from rag.retriever import retrieve_policy

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
import json

def decision_node(state):
    if not state["messages"]:
        prompt = f"""
        You are an automated Travel Reimbursement Approval Agent.

        Your responsibility is to evaluate an employee travel reimbursement claim by using the retrieved company policy and the provided validation tools.

        Do NOT ask the user for additional information.
        Do NOT assume missing values.
        Use the claim below as the only source of truth.

        Policy:
        {state["policy_context"]}

        Claim:
        {json.dumps(state["claim"], indent=2)}

        Before generating the final response, you MUST execute ALL of the following tools exactly once:

        1. receipt_checker(receipt_attached)
        2. limit_checker(stay, food, travel)
        3. approval_checker(stay, food, travel, manager_approval, director_approval)

        Wait until all tool results are available before making any decision.

        Decision Rules:

        1. APPROVED
        - All required validations pass.
        - No reimbursement amount is rejected.

        2. PARTIALLY_APPROVED
        - Some expenses exceed reimbursement limits.
        - Part of the claim is approved and the remaining amount is rejected.

        3. REJECTED
        - The entire reimbursement claim must be rejected.
        - Examples:
            • Required approvals are missing.
            • Required receipts are missing.
            • The policy does not allow reimbursement.

        4. MANUAL_REVIEW
        - Information is incomplete.
        - Tool results conflict.
        - The policy cannot determine a clear decision.

        IMPORTANT:

        Your FIRST LINE must ALWAYS be exactly one of the following:

        Decision: APPROVED

        OR

        Decision: PARTIALLY_APPROVED

        OR

        Decision: REJECTED

        OR

        Decision: MANUAL_REVIEW

        After the decision line, provide a short explanation including:

        - Receipt Status
        - Approval Status
        - Approved Amount
        - Rejected Amount
        - Policy reasoning
        """
    
        messages = [HumanMessage(content=prompt)]


    else:
        messages=state["messages"]

    response = llm_with_tools.invoke(messages)
    

    return {
        "messages": [response],
        "audit_log": state["audit_log"] + ["Agent executed"]
    }

#----------Node 3: Output Node--------
from models.output_schema import DecisionOutput
import json
from langchain_core.messages import ToolMessage

def output_node(state):

    approved_amount = None
    rejected_amount = None
    missing_documents = []
    policy_reference = []
    approval_status = None
    for message in state["messages"]:

        if not isinstance(message, ToolMessage):
            continue

        data = json.loads(message.content)

        if message.name == "receipt_checker":
            missing_documents = data.get("missing_documents", [])

        elif message.name == "limit_checker":
            approved_amount = data.get("approved_amount")
            rejected_amount = data.get("rejected_amount")

        elif message.name == "approval_checker":
            approval_status = data.get("status")

    final_message = state["messages"][-1].content

    decision = "MANUAL_REVIEW"

    if final_message:

        first_line = final_message.split("\n")[0].strip().upper()

        if "PARTIALLY_APPROVED" in first_line:
            decision = "PARTIALLY_APPROVED"

        elif "MANUAL_REVIEW" in first_line:
            decision = "MANUAL_REVIEW"

        elif "REJECTED" in first_line:
            decision = "REJECTED"

        elif "APPROVED" in first_line:
            decision = "APPROVED"


    confidence = 1.0

    if missing_documents:
        confidence -= 0.20

    if approval_status == "FAIL":
        confidence -= 0.15

    if not state["policy_context"]:
        confidence -= 0.20

    if decision == "MANUAL_REVIEW":
        confidence -= 0.20

    confidence = round(max(0.0, min(confidence, 1.0)), 2)
    
    result = DecisionOutput(
        decision=decision,
        approved_amount=approved_amount,
        rejected_amount=rejected_amount,
        missing_documents=missing_documents,
        policy_reference=policy_reference,
        confidence=confidence,
        explanation=final_message
    )

    state["decision"] = result.model_dump()

    state["audit_log"].append("Structured output generated")

    return state