import json
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.secret')

# Configuration
file_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/freepublic-apis/agent/freepublic-apis.json'
output_file = '/Users/chenzi/project/zcbc/mofa/python/examples/dataflow_mcp/generated_public_api_server.py'

# Initialize OpenAI client with environment variables
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('LLM_BASE_URL', 'https://api.openai.com/v1')
)

def read_json_lines(file_path):
    """Read JSON lines from file"""
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def sanitize_name(name):
    """Convert API name to valid Python function name"""
    # Remove special characters and replace with underscores
    name = re.sub(r'[^\w\s-]', '', name.lower())
    name = re.sub(r'[-\s]+', '_', name)
    name = re.sub(r'^_+|_+$', '', name)
    # Ensure it doesn't start with a number
    if name and name[0].isdigit():
        name = 'api_' + name
    return name

def generate_function_name(api_name, endpoint_index=0):
    """Generate unique function name from API name"""
    base_name = sanitize_name(api_name)
    if endpoint_index > 0:
        return f"{base_name}_{endpoint_index}"
    return base_name

def create_mcp_tool_prompt(api_data, endpoint_data, function_name):
    """Create prompt for LLM to generate MCP tool"""
    prompt = f"""
Generate a FastMCP tool function for the following API endpoint:

API Name: {api_data['url'].split('/')[-1].replace('-', ' ').title()}
Endpoint: {endpoint_data['endpoint']}
Description: {endpoint_data['description']}
Method: {endpoint_data['request_type']}
Parameters: {endpoint_data['request_parameter']}
Documentation: {endpoint_data['documentation_url']}

Create a Python async function that wraps this API endpoint as a FastMCP tool. 

Requirements:
1. Use @mcp.tool() decorator with appropriate name and description
2. Include proper async/await syntax
3. Handle errors gracefully with try/catch
4. Use requests library for HTTP calls
5. Add appropriate parameter validation
6. Return structured JSON response
7. Add Chinese descriptions where appropriate
8. Follow FastMCP patterns from the example

Function signature should be:
async def {function_name}(ctx: Context, ...)

Generate only the function code, no explanations.
"""
    return prompt

def generate_mcp_server_header():
    """Generate the MCP server header code"""
    return '''#!/usr/bin/env python3
"""
Generated FastMCP Server for Free Public APIs
This file contains MCP tools for various free public APIs.
"""

import json
import asyncio
import requests
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from fastmcp.server.context import Context

# Initialize FastMCP server
mcp = FastMCP(name="free-public-apis-server", description="Free public APIs as MCP tools")

'''

def generate_mcp_server_footer():
    """Generate the MCP server footer code"""
    return '''
if __name__ == "__main__":
    print("Starting Free Public APIs MCP Server...")
    print(f"Total tools: {len([f for f in dir() if not f.startswith('_') and callable(globals()[f])]) - 3}")  # Rough count
    
    # Start the server
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1", 
        port=9001
    )
'''

def generate_tool_with_llm(prompt):
    """Use LLM to generate MCP tool code - currently using fallback due to auth issues"""
    # Skip LLM generation and use fallback for now
    return None

def create_fallback_tool(api_data, endpoint_data, function_name):
    """Create a fallback tool if LLM generation fails"""
    endpoint = endpoint_data['endpoint']
    description = endpoint_data['description']
    method = endpoint_data['request_type']
    
    # Extract parameters from request_parameter
    params_str = endpoint_data['request_parameter']
    params = []
    if params_str and params_str != 'None' and params_str != 'Not specified':
        if '=' in params_str:
            param_parts = params_str.split(',')
            for part in param_parts:
                if '=' in part:
                    param_name = part.split('=')[0].strip()
                    if param_name not in ['None', 'Not specified']:
                        # Replace hyphens with underscores in parameter names
                        param_name = param_name.replace('-', '_')
                        params.append(param_name)
    
    # Build parameter string
    param_signature = ""
    param_usage = ""
    if params:
        param_signature = ", " + ", ".join([f"{p}: str = ''" for p in params])
        param_usage = ", ".join([f"\"{p}\": {p}" for p in params if p])
    
    # Escape quotes in description
    safe_description = description[:100].replace("'", "\\'").replace('"', '\\"')
    safe_docstring = description.replace("'", "\\'").replace('"', '\\"')
    
    tool_code = f'''
@mcp.tool(
    name=\'{function_name}\',
    description=\'{safe_description}...\'
)
async def {function_name}(ctx: Context{param_signature}) -> dict:
    """
    {safe_docstring}
    """
    print(f"[FastMCP工具] {function_name}() called")
    
    try:
        url = "{endpoint}"
        params = {{{param_usage}}}
        
        response = requests.{method.lower()}(url, params=params if params else None, timeout=10)
        response.raise_for_status()
        
        return {{
            "data": response.json(),
            "source": "{endpoint}",
            "status_code": response.status_code
        }}
        
    except requests.exceptions.RequestException as e:
        await ctx.error(f"API请求失败: {{str(e)}}")
        return {{"error": f"API请求失败: {{str(e)}}", "source": "{endpoint}"}}
    except json.JSONDecodeError:
        return {{
            "data": response.text,
            "source": "{endpoint}",
            "status_code": response.status_code,
            "note": "返回非JSON格式数据"
        }}
    except Exception as e:
        await ctx.error(f"处理响应失败: {{str(e)}}")
        return {{"error": f"处理响应失败: {{str(e)}}", "source": "{endpoint}"}}

'''
    return tool_code

def main():
    """Main function to generate MCP server"""
    print("Reading freepublic-apis.json...")
    apis_data = read_json_lines(file_path)
    print(f"Found {len(apis_data)} API entries")
    
    # Generate server code
    server_code = generate_mcp_server_header()
    
    tool_count = 0
    
    for api_idx, api_data in enumerate(apis_data):
        if api_data.get('success') and api_data.get('data'):
            for endpoint_idx, endpoint in enumerate(api_data['data']):
                if endpoint.get('error') is False:
                    # Generate unique function name
                    api_name = api_data['url'].split('/')[-1].replace('-', '_')
                    function_name = generate_function_name(api_name, endpoint_idx)
                    
                    print(f"Generating tool {tool_count+1}: {function_name}")
                    
                    # Create prompt for LLM
                    prompt = create_mcp_tool_prompt(api_data, endpoint, function_name)
                    
                    # Generate tool with LLM
                    tool_code = generate_tool_with_llm(prompt)
                    
                    if tool_code:
                        server_code += tool_code + "\n\n"
                    else:
                        # Use fallback
                        print(f"Using fallback for {function_name}")
                        tool_code = create_fallback_tool(api_data, endpoint, function_name)
                        server_code += tool_code
                    
                    tool_count += 1
                    
                    # Add small delay to avoid rate limiting
                    if tool_count % 5 == 0:
                        print(f"Generated {tool_count} tools so far...")
    
    # Add footer
    server_code += generate_mcp_server_footer()
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(server_code)
    
    print(f"\nMCP server generated successfully!")
    print(f"Total tools generated: {tool_count}")
    print(f"Output file: {output_file}")

if __name__ == "__main__":
    main()


