from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Optional

from app.tools.fetch_nse import get_nse_stock_info
from app.tools.fetch_bse import get_bse_stock_info
from app.tools.formatter import format_response_with_llm

# Define the agent's state schema
class AgentState(TypedDict):
    input: str
    output: Optional[str]


def build_stock_agent():
    # Tool logic with proper docstring
    def agent_tool(state: AgentState) -> AgentState:
        """
        Fetches stock information for a given symbol from NSE and BSE, then formats it.

        Args:
            state (AgentState): The agent state dictionary containing:
                - 'input': the stock symbol as a string.

        Returns:
            AgentState: Updated state with:
                - 'input': same stock symbol
                - 'output': an LLM-formatted string with LTP, market cap, 52-week high/low, and last quarter results.
        """
        stock_symbol = state.get("input", "").strip().upper()

        # Scrape data from NSE and BSE
        nse_data = get_nse_stock_info(stock_symbol)
        bse_data = get_bse_stock_info(stock_symbol)

        combined_data = {
            "NSE": nse_data,
            "BSE": bse_data
        }

        # Format the combined data using the LLM
        formatted_response = format_response_with_llm(combined_data)

        return {
            "input": stock_symbol,
            "output": formatted_response
        }

    # Build graph with state schema
    builder = StateGraph(AgentState)
    # Register the tool node with a list containing the function
    builder.add_node("fetch_and_format", ToolNode([agent_tool]))
    # Define entry and finish points
    builder.set_entry_point("fetch_and_format")
    builder.set_finish_point("fetch_and_format")

    # Compile and return the agent
    return builder.compile()
