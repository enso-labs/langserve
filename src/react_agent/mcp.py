import json
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

class MCPClient:
    def __init__(self):
        self.mcp_client = None
        
    def get_client(self):
        self.mcp_client = MultiServerMCPClient(self.get_mcp_config().get("mcp", {}))
        # return self.mcp_client
    
    async def setup(self):    
        self.get_client()
        await self.mcp_client.__aenter__()
        
    async def cleanup(self):
        if self.mcp_client:
            await self.mcp_client.__aexit__(None, None, None)
        
    def get_mcp_config(self):
        with open("mcp.json", "r") as f:
            mcp_config = json.load(f)
        return mcp_config
        
    async def get_tools(self):
        await self.setup()
        tools = self.mcp_client.get_tools()
        await self.cleanup()
        return tools
        