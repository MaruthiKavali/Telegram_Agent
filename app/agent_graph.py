from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from typing import TypedDict

from app.tools.fetch_nse import get_nse_stock_info
from app.tools.fetch_bse import get_bse_stock_info
from app.tools.formatter import format_response_with_llm

class AgentState(TypedDict):
    input: str
    output: str

def build_stock_agent():
    def agent_tool(state: AgentState) -> AgentState:
        stock_name = state["input"]

        nse_data = get_nse_stock_info(stock_name)
        bse_data = get_bse_stock_info(stock_name)

        combined_data = {
            "NSE": nse_data,
            "BSE": bse_data
        }

        formatted_response = format_response_with_llm(combined_data)

        return {
            "input": stock_name,
            "output": formatted_response
        }

    builder = StateGraph(AgentState)
    builder.add_node("fetch_and_format", ToolNode([agent_tool]))
    builder.set_entry_point("fetch_and_format")
    builder.set_finish_point("fetch_and_format")

    return builder.compile()
