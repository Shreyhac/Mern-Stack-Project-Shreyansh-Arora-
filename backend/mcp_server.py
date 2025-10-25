#!/usr/bin/env python3
"""
MCP Server for Web to MCP
Provides captured website components to Cursor via MCP protocol
"""

import json
import asyncio
import sys
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, 
    Tool, 
    TextContent, 
    ImageContent,
    EmbeddedResource
)

# Import our demo server's storage
import sys
import os
sys.path.append(os.path.dirname(__file__))
from demo_server import captures_storage

# Create MCP server
server = Server("web-to-mcp")

@server.list_resources()
async def list_resources() -> List[Resource]:
    """List all available captured components"""
    resources = []
    
    for capture_id, capture_data in captures_storage.items():
        resources.append(Resource(
            uri=f"web-to-mcp://capture/{capture_id}",
            name=f"Component from {capture_data.get('domain', 'unknown')}",
            description=f"Captured component from {capture_data.get('website_url', 'unknown')}",
            mimeType="application/json"
        ))
    
    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific captured component"""
    if not uri.startswith("web-to-mcp://capture/"):
        raise ValueError(f"Invalid URI: {uri}")
    
    capture_id = uri.split("/")[-1]
    
    if capture_id not in captures_storage:
        raise ValueError(f"Capture {capture_id} not found")
    
    capture_data = captures_storage[capture_id]
    
    # Format the data for Cursor
    formatted_data = {
        "id": capture_data["id"],
        "website_url": capture_data["website_url"],
        "domain": capture_data["domain"],
        "token_count": capture_data["token_count"],
        "created_at": capture_data["created_at"],
        "html": capture_data["html"],
        "screenshot": capture_data["screenshot"],
        "analysis": {
            "component_type": "Web Component",
            "source": capture_data["domain"],
            "capture_method": "Browser Extension",
            "data_format": "HTML + Screenshot"
        }
    }
    
    return json.dumps(formatted_data, indent=2)

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="analyze_component",
            description="Analyze a captured web component",
            inputSchema={
                "type": "object",
                "properties": {
                    "capture_id": {
                        "type": "string",
                        "description": "The capture ID to analyze"
                    }
                },
                "required": ["capture_id"]
            }
        ),
        Tool(
            name="list_captures",
            description="List all available captures",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    if name == "analyze_component":
        capture_id = arguments.get("capture_id")
        if not capture_id:
            return [TextContent(type="text", text="Error: capture_id is required")]
        
        if capture_id not in captures_storage:
            return [TextContent(type="text", text=f"Error: Capture {capture_id} not found")]
        
        capture_data = captures_storage[capture_id]
        
        analysis = f"""
# Component Analysis

**Capture ID:** {capture_data['id']}
**Website:** {capture_data['website_url']}
**Domain:** {capture_data['domain']}
**Token Count:** {capture_data['token_count']}
**Created:** {capture_data['created_at']}

## HTML Structure
```html
{capture_data['html'][:1000]}{'...' if len(capture_data['html']) > 1000 else ''}
```

## Analysis
This component was captured from {capture_data['domain']} and contains {capture_data['token_count']} tokens.
The HTML structure shows the component's markup and styling information.

## Usage in Cursor
You can use this captured component as a reference for:
- Understanding the component structure
- Recreating similar components
- Analyzing styling and layout
- Learning from real-world implementations
"""
        
        return [TextContent(type="text", text=analysis)]
    
    elif name == "list_captures":
        if not captures_storage:
            return [TextContent(type="text", text="No captures available")]
        
        capture_list = "## Available Captures\n\n"
        for capture_id, capture_data in captures_storage.items():
            capture_list += f"- **{capture_id}** from {capture_data['domain']} ({capture_data['created_at']})\n"
        
        return [TextContent(type="text", text=capture_list)]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="web-to-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
