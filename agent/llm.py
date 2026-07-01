"""
LLM configuration.
"""

from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI

from tools.receipt_checker import receipt_checker
from tools.limit_checker import limit_checker
from tools.approval_checker import approval_checker
load_dotenv()

llm = ChatOpenAI(
    model="openrouter/free",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE_URL"),
    temperature=0
)

llm_with_tools = llm.bind_tools(
    [
        receipt_checker,
        limit_checker,
        approval_checker
    ]
)

# print("\nReceipt Checker Schema")
# print(receipt_checker.args)

# print("\nLimit Checker Schema")
# print(limit_checker.args)

# print("\nApproval Checker Schema")
# print(approval_checker.args)