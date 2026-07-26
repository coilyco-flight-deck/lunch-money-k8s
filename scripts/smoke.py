"""Import the server and print its registered MCP tool names."""

from lunch_money_mcp import server


tool_names = sorted(tool.name for tool in server.mcp._tool_manager.list_tools())
print("tools:", tool_names)
