import json
from agent.graph import workflow

with open("data/claims.json") as f:
    claims = json.load(f)

print("\nAvailable Claims:")
for claim in claims:
    print(f"Claim ID: {claim['claim_id']}")

claim_id = int(input("\nEnter Claim ID: "))

claim = next(
    (c for c in claims if c["claim_id"] == claim_id),
    None
)

if claim is None:
    print("Invalid Claim ID")
    exit()

initial_state = {
    "claim": claim,
    "messages": [],
    "policy_context": "",
    "decision": {},
    "audit_log": []
}

result = workflow.invoke(
    initial_state,
    config={"recursion_limit": 10}
)

print("\nDecision:\n")
print(json.dumps(result["decision"], indent=4))

print("\nAudit Log:\n")
for item in result["audit_log"]:
    print(f"- {item}")