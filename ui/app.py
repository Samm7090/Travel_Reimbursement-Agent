import streamlit as st
import json

from agent.graph import workflow

st.title("Travel Reimbursement Approval Agent")

input_method = st.radio(
    "Choose Input Method",
    ["Upload JSON File", "Paste JSON"]
)

claim = None

# ---------------- Upload JSON ---------------- #

if input_method == "Upload JSON File":

    uploaded_file = st.file_uploader(
        "Upload Claim JSON",
        type=["json"]
    )

    if uploaded_file:

        claims = json.load(uploaded_file)

        # Multiple claims
        if isinstance(claims, list):

            employee_ids = [c["employee_id"] for c in claims]

            selected_employee = st.selectbox(
                "Select Employee",
                employee_ids
            )

            claim = next(
                c for c in claims
                if c["employee_id"] == selected_employee
            ) 

        # Single claim
        else:
            claim = claims

# ---------------- Manual JSON ---------------- #

else:

    json_text = st.text_area("Paste Claim JSON", height=300)

    if json_text:

        try:
            claim = json.loads(json_text)

        except Exception as e:
            st.error(f"Invalid JSON\n\n{e}")

# ---------------- Run Workflow ---------------- #

if claim:

    if st.button("Evaluate Claim"):

        initial_state = {
            "claim": claim,
            "messages": [],
            "policy_context": "",
            "decision": {},
            "audit_log": []
        }

        result = workflow.invoke(initial_state,config={"recursion_limit": 10})

        st.subheader("Decision")
        st.json(result["decision"])

        st.subheader("Audit Log")
        st.write(result["audit_log"])