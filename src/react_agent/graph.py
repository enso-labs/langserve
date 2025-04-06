# graph.py
import asyncio
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from react_agent.mcp import MCPClient
from react_agent.tools import TOOLS

session = MCPClient()
model = ChatAnthropic(model="claude-3-5-sonnet-latest")

@asynccontextmanager
async def make_graph():
    async with MultiServerMCPClient(session.get_mcp_config().get("mcp", {})) as client:
        TOOLS.extend(client.get_tools())
        agent = create_react_agent(model, TOOLS)
        yield agent
