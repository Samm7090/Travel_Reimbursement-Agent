## Table of Contents

- Project Overview
- Features
- Technology Stack
- System Architecture
- Project Workflow
- LangGraph Workflow
- Shared Graph State
- Business Validation Tools
- RAG Pipeline
- Design Decisions
- Assumptions
- Limitations
- Future Enhancements
- Project Structure
- Installation
- Running the Application
- Sample Input
- Sample Output


# Travel Reimbursement Approval Agent

## Project Overview

    An Agentic AI-powered Travel Reimbursement Approval System built using **LangGraph**, **LangChain**, **Ollama (Qwen3:4B)**, and **Retrieval-Augmented Generation (RAG)**.

    The application automates the evaluation of employee travel reimbursement claims by combining policy retrieval, LLM reasoning, and business rule validation through tool calling. It accepts reimbursement claims in JSON format, retrieves relevant sections of the company travel policy using a FAISS-based vector store, invokes multiple validation tools, and generates a structured reimbursement decision.

    The system follows an Agentic AI workflow where the Large Language Model (LLM) determines when to invoke business validation tools such as receipt verification, reimbursement limit checking, and approval hierarchy validation before producing a final decision.

    The final response includes the reimbursement decision, approved and rejected amounts, missing documents, confidence score, explanation, and an audit trail describing the execution flow.

## Project Features

    - Accepts travel reimbursement claims through JSON upload or manual JSON input.
    - Supports evaluation of multiple employee claims by selecting an Employee ID.
    - Uses Retrieval-Augmented Generation (RAG) to retrieve relevant reimbursement policies before making a decision.
    - Implements an Agentic AI workflow using LangGraph where the LLM autonomously decides when to invoke business validation tools.
    - Validates receipt availability for reimbursement claims.
    - Verifies claimed expenses against reimbursement limits defined in the company policy.
    - Checks approval hierarchy based on configurable approval thresholds.
    - Produces structured reimbursement decisions including:
    - Decision (Approved / Partially Approved / Rejected / Manual Review)
    - Approved Amount
    - Rejected Amount
    - Missing Documents
    - Confidence Score
    - Decision Explanation
    - Maintains an audit trail of the execution workflow for explainability.
    - Provides both a Command Line Interface (CLI) and a lightweight Streamlit web interface for demonstration.

## Technology Stack

    | Component | Technology |
    |-----------|------------|
    | Programming Language | Python 3.13 |
    | Agent Framework | LangGraph |
    | LLM Framework | LangChain |
    | Large Language Model | Ollama (Qwen3:4B) |
    | Retrieval | FAISS |
    | Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
    | User Interface | Streamlit |
    | Data Format | JSON |
    | Schema Validation | Pydantic |

## System Architecture
    '''text

        JSON Claim
            │
            ▼
        CLI / Streamlit
            │
            ▼
        Retrieve Policy Node
            │
            ▼
        FAISS Retriever
            ▲
            │
        Travel Policy.md
            │
            ▼
        Decision Node (LLM)
            │
            ▼
        ToolNode
        ├──────────────┐
        │Receipt Check │
        │Limit Check   │
        │Approval Check│
        └──────────────┘
            │
            ▼
        Decision Node
            │
            ▼
        Output Node
            │
            ▼
        Pydantic Output
            │
        ┌────┴─────────┐
        ▼              ▼
        Decision     Audit Log
    '''

## Project Workflow

    ```text
    1. Employee uploads a reimbursement claim in JSON format.

    2. The system retrieves relevant reimbursement policies using RAG.

    3. The LangGraph agent analyzes the claim and policy context.

    4. The LLM determines which business validation tools need to be executed.

    5. ToolNode executes:
    • Receipt Checker
    • Expense Limit Checker
    • Approval Checker

    6. Tool results are returned to the LLM.

    7. The LLM generates the final reimbursement decision.

    8. The output node converts the response into a structured format.

    9. Results are displayed through the CLI or Streamlit interface.
    ```

## LangGraph Execution Flow

    The workflow follows the execution sequence below:

    1. Retrieve Policy Node retrieves relevant reimbursement policies using RAG.
    2. The Decision Node prepares the LLM prompt using the claim and retrieved policy.
    3. The LLM determines which business validation tools should be invoked.
    4. ToolNode executes:
    - Receipt Checker
    - Limit Checker
    - Approval Checker
    5. Tool outputs are returned to the Decision Node.
    6. The LLM generates the final reimbursement explanation.
    7. The Output Node converts the response into a validated Pydantic object.
    8. The structured response is returned to the user.

## LangGraph Workflow

    The application is implemented using **LangGraph**, where each step of the reimbursement evaluation process is represented as an independent node. The graph manages the execution flow, allowing the LLM to retrieve policy context, invoke validation tools, and generate a structured reimbursement decision.

    ### Workflow Nodes

    ### 1. Retrieve Policy Node
    - Receives the employee reimbursement claim.
    - Identifies applicable expense categories (Stay, Food, Travel).
    - Generates a retrieval query dynamically.
    - Retrieves the most relevant reimbursement policy sections from the FAISS vector store.
    - Stores the retrieved policy context in the shared graph state.

    ### 2. Decision Node
    - Constructs a prompt using:
    - Employee reimbursement claim
    - Retrieved policy context
    - Invokes the LLM.
    - The LLM autonomously determines which business validation tools should be executed.
    - Receives tool outputs and generates the final reimbursement explanation.

    ### 3. ToolNode
    The ToolNode executes the business validation tools requested by the LLM.

    Implemented tools include:

    - Receipt Checker
    - Expense Limit Checker
    - Approval Hierarchy Checker

    ### 4. Output Node
    The Output Node converts the LLM response into a structured JSON output using a Pydantic schema.

    The final response includes:

    - Decision
    - Approved Amount
    - Rejected Amount
    - Missing Documents
    - Policy References
    - Confidence Score
    - Explanation

    The node also records the execution audit trail for explainability.

## Shared Graph State

    The workflow uses a shared state object that is passed between every node in the graph.

    The state maintains:

    | Field | Purpose |
    |--------|---------|
    | `claim` | Employee reimbursement claim |
    | `policy_context` | Retrieved reimbursement policy |
    | `messages` | Conversation history exchanged with the LLM |
    | `decision` | Final structured reimbursement decision |
    | `audit_log` | Execution history for explainability |

    Using a shared state allows every node to access the outputs generated by previous nodes without tightly coupling the implementation.

## Business Validation Tool

    The reimbursement agent uses modular business validation tools implemented using LangChain Tool Calling.

    ### Receipt Checker

    Validates whether the required reimbursement receipt has been attached.

    **Output**

    - PASS
    - FAIL
    - Missing Documents

    ---

    ### Expense Limit Checker

    Compares claimed expenses against reimbursement limits defined in the policy.

    Calculates:

    - Approved Amount
    - Rejected Amount
    - Expense Breakdown
    - Policy Violations

    ---

    ### Approval Hierarchy Checker

    Validates whether the required approvals are available based on configurable reimbursement thresholds.

    Business Rules:

    - Claims above Manager Threshold require Manager Approval.
    - Claims above Director Threshold require Director Approval.

## RAG Pipeline

    To ensure reimbursement decisions are grounded in company policy rather than relying solely on the LLM's internal knowledge, the application uses Retrieval-Augmented Generation (RAG).

    ### Retrieval Pipeline

    1. Load the travel reimbursement policy document.
    2. Split the document into smaller chunks using Recursive Character Text Splitting.
    3. Generate vector embeddings using the **sentence-transformers/all-MiniLM-L6-v2** embedding model.
    4. Store embeddings in a FAISS vector database.
    5. Retrieve the most relevant policy chunks based on the reimbursement categories present in the employee claim.
    6. Provide the retrieved policy context to the LLM before business reasoning begins.

    This approach ensures that reimbursement decisions remain grounded in organizational policy and can easily adapt when the policy document changes.

## Design Decisions

    Several design choices were made to keep the prototype lightweight, modular, and aligned with the assignment requirements.

    ### LangGraph

    LangGraph was selected to orchestrate the reimbursement workflow because it provides a clear representation of multi-step AI workflows. Each stage of the reimbursement process is implemented as an independent node, making the workflow modular, maintainable, and easy to extend.

    ### Retrieval-Augmented Generation (RAG)

    Instead of relying solely on the LLM's internal knowledge, reimbursement policies are retrieved dynamically using RAG. This ensures that reimbursement decisions remain grounded in company policy and allows policy updates without modifying application logic.

    ### Tool Calling

    Business validations such as receipt verification, expense limit validation, and approval hierarchy checks are implemented as independent tools. This separates deterministic business logic from LLM reasoning and makes the solution easier to maintain and test.

    ### Structured Output

    A Pydantic schema is used to validate the final reimbursement decision before returning it to the user. This guarantees a consistent output structure regardless of the LLM response.

    ### Ollama

    The application uses a locally hosted Ollama model to provide an offline, cost-effective solution without requiring paid API access. The architecture remains compatible with cloud-hosted LLMs such as OpenAI or Anthropic for production deployments.

## Assumptions

    The following assumptions were made while developing this prototype:

    - The uploaded reimbursement claim contains all required claim information.
    - Only one reimbursement claim is evaluated per employee in the sample dataset.
    - Company reimbursement policies are represented using a sample Markdown document.
    - Expense limits and approval thresholds are stored in static JSON configuration files.
    - Receipt availability is represented as a boolean field in the claim data.
    - The prototype focuses on reimbursement evaluation and does not include authentication or employee management.
    - Manual Review is returned whenever the available information is insufficient for an automated decision.

## Limitations

    This project is intended as a functional prototype and includes the following limitations:

    - Uses mock reimbursement policies and sample claim data.
    - Receipt validation checks only attachment availability and does not perform OCR or document verification.
    - Duplicate reimbursement detection is not implemented and can be added as a separate validation tool.
    - The current implementation uses a local Ollama model. While suitable for demonstration, larger production-grade models may provide more reliable tool-calling behavior.
    - The vector database is recreated during application startup rather than persisted.
    - The application does not integrate with external HRMS, ERP, or finance systems.
    - User authentication and role-based access control are outside the scope of this prototype.

## Future Enhancements

    Potential improvements for a production-ready implementation include:

    - Persistent vector database for policy management.
    - OCR-based receipt extraction and validation.
    - Duplicate reimbursement claim detection as a dedicated validation tool.
    - Integration with ERP or HRMS platforms through REST APIs.
    - Human-in-the-loop approval workflow for Manual Review cases.
    - Email and notification integration for reimbursement decisions.
    - Policy versioning and automatic policy synchronization.
    - Multi-user authentication with role-based access control.
    - Deployment using Docker and cloud infrastructure.
    - Support for Model Context Protocol (MCP) to integrate external enterprise tools.

## Folder Structure

    ```text
    travel-reimbursement-agent/
    │
    ├── agent/
    │   ├── graph.py
    │   ├── llm.py
    │   ├── nodes.py
    │   └── state.py
    │
    ├── data/
    │   ├── approval_matrix.json
    │   ├── claims.json
    │   ├── limits.json
    │   └── travel_policy.md
    │
    ├── models/
    │   └── output_schema.py
    │
    ├── rag/
    │   └── retriever.py
    │
    ├── tools/
    │   ├── approval_checker.py
    │   ├── limit_checker.py
    │   └── receipt_checker.py
    │
    ├── ui/
    │   └── app.py
    │
    ├── app.py
    ├── pyproject.toml
    └── README.md
    ```

## Installation

    ### Clone the Repository

    ```bash
    git clone https://github.com/Samm7090/Travel_Reimbursement-Agent.git

    cd travel-reimbursement-agent
    ```

    ### Create Virtual Environment

    ```bash
    python -m venv .venv
    ```

    ### Activate Virtual Environment

    Windows

    ```bash
    .venv\Scripts\activate
    ```

    Linux / macOS

    ```bash
    source .venv/bin/activate
    ```

    ### Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

    ### Install Ollama

    Download and install Ollama from:

    https://ollama.com

    Pull the model used in this project:

    ```bash
    ollama pull qwen3:4b
    ```

## Running the Application
  
    ### Command Line Interface

    ```bash
    python app.py
    ```

    ### Streamlit Web Interface

    ```bash
    python -m streamlit run ui/app.py
    ```

    The Streamlit interface supports:

    - Uploading reimbursement claim JSON files
    - Selecting an employee claim
    - Manually pasting reimbursement claim JSON
    - Viewing structured reimbursement decisions
    - Viewing workflow audit logs

## Sample Input
  
    ```json
    {
    "employee_id": "EMP001",
    "stay": 120,
    "food": 40,
    "travel": 50,
    "receipt_attached": true,
    "manager_approval": true,
    "director_approval": false
    }
    ```

## Sample Output
  
    ```json
    {
    "decision": "APPROVED",
    "approved_amount": 210.0,
    "rejected_amount": 0.0,
    "missing_documents": [],
    "policy_reference": [],
    "confidence": 1.0,
    "explanation": "All expenses are within policy limits and approval requirements have been satisfied."
    }
    ```