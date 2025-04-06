import json
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

class MCPClient:
    def __init__(self):
        self.mcp_client = None
        self.agent = None
        
    def get_mcp_config(self):
        with open("mcp.json", "r") as f:
            mcp_config = json.load(f)
        return mcp_config
        
    async def get_tools(self):
        tools = []
        async with MultiServerMCPClient(self.get_mcp_config().get("mcp", {})) as mcp_client:
            tools = mcp_client.get_tools()
        return tools
        