"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

import asyncio
from typing import Any, Callable, List, Optional, cast
import os
from langchain_core.tools import tool, ToolException
from browser_use import Agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolArg
from typing_extensions import Annotated
from langchain_anthropic import ChatAnthropic

from react_agent.configuration import Configuration

@tool
async def search(
    query: str, *, config: Annotated[RunnableConfig, InjectedToolArg]
) -> Optional[list[dict[str, Any]]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_runnable_config(config)
    wrapped = TavilySearchResults(max_results=configuration.max_search_results)
    result = await wrapped.ainvoke({"query": query})
    return cast(list[dict[str, Any]], result)

@tool
def browser_use(task: str, model: str = 'claude-3-7-sonnet-latest'):
    """Use the browser to perform a task. Rewrite the task to be more specific and concise. Be sure to include all necessary steps, details, and context.
    
    Example:
        .. code-block:: python
        
            response = browser_use(
                task="Go to Reddit, search for 'browser-use', click on the first post and return the first comment.",
            )
    
    Args:
        task (str): The task to be performed
        
    Returns:
        str: The formatted result of the task
    """
    try:
        llm = ChatAnthropic(model=model, api_key=os.getenv('ANTHROPIC_API_KEY'))
        agent = Agent(
            task=task,
            llm=llm,
        )
        import asyncio
        result = asyncio.run(agent.run())
        action_results = result.action_results()
        
        # Format the results as a string
        formatted_string = ""
        for i, res in enumerate(action_results):
            res_dict = dict(res)
            formatted_string += f"Result {i+1}:\n"
            
            # Handle extracted content specially if it exists
            if 'extracted_content' in res_dict and res_dict['extracted_content']:
                formatted_string += f"  Content: {res_dict['extracted_content']}\n"
                
            # Add other important fields
            if 'is_done' in res_dict:
                formatted_string += f"  Status: {'Completed' if res_dict['is_done'] else 'Incomplete'}\n"
                
            if 'error' in res_dict and res_dict['error']:
                formatted_string += f"  Error: {res_dict['error']}\n"
                
            formatted_string += "\n"
            
        return formatted_string.strip()
    except Exception as e:
        raise ToolException(f"Error running browser_use: {str(e)}")


import yfinance as yf

@tool
def get_stock_price(ticker: str) -> str:
    """Get the current price of a stock using its ticker symbol.
    
    Example:
        .. code-block:: python
            
            response = get_stock_price("AAPL")
    
    Args:
        ticker (str): The stock ticker symbol (e.g. "AAPL" for Apple)
        
    Returns:
        str: The current stock price formatted as a string
    """
    try:
        # Create a Ticker object
        stock = yf.Ticker(ticker)
        
        # Fetch the current price using fast_info
        current_price = stock.fast_info['last_price']
        
        return f"The current price of {ticker} is: ${current_price:.2f}"
    except Exception as e:
        raise ToolException(f"Error getting stock price: {str(e)}")
    
    
from react_agent.mcp import MCPClient
session = MCPClient()

TOOLS: List[Callable[..., Any]] = [browser_use, search, get_stock_price]

mcp_tools = asyncio.run(session.get_tools())
TOOLS.extend(mcp_tools)
