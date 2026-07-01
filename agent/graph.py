from langgraph.graph import StateGraph
from langgraph.graph import END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from tools.receipt_checker import receipt_checker
from tools.limit_checker import limit_checker
from tools.approval_checker import approval_checker


tools = [receipt_checker, limit_checker, approval_checker]
tool_node = ToolNode(tools)

from agent.state import AgentState
from agent.nodes import retreieve_policy,decision_node, output_node

graph = StateGraph(AgentState)

graph.add_node("retrieve_policy",retreieve_policy)
graph.add_node("agent",decision_node)
graph.add_node("tools",tool_node)
graph.add_node("output",output_node)

graph.set_entry_point("retrieve_policy")
graph.add_edge("retrieve_policy","agent")
graph.add_conditional_edges("agent",tools_condition)
graph.add_edge("tools","agent")
graph.add_edge("agent","output")
graph.add_edge("output",END)

workflow = graph.compile()