import json
from agent.graph import workflow
from langchain_core.messages import HumanMessage

with open("data/claims.json") as f:
    claims = json.load(f)
claim=claims[0]

initial_state = {

    "claim": claim,
    "messages": [],
    "policy_context": "",
    "decision": {},
    "audit_log": []
}

result = workflow.invoke(initial_state, config={"recursion_limit": 10})

# print("\nFULL STATE")
# print(result)

# print("\nDecision:\n")
# print(result["messages"][-1].content)

print("\nAudit Log:\n")
for item in result["audit_log"]:
    print(item)