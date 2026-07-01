"""
LLM configuration.
"""


from tools.receipt_checker import receipt_checker
from tools.limit_checker import limit_checker
from tools.approval_checker import approval_checker


from dotenv import load_dotenv
import os

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:4b")


from langchain_ollama import ChatOllama

llm = ChatOllama(
    model=MODEL_NAME, 
    temperature=0
)

llm_with_tools = llm.bind_tools(
    [
        receipt_checker,
        limit_checker,
        approval_checker
    ]
)
