import json
from tools import document_tools

# no raw eval or exec
TOOL_FUNCTIONS = {
    #tools
        #recent_documents
    "get_recent_documents": document_tools.get_recent_documents,

}

def execute_tool_call(tool_call_json: str) -> str:
    """
    Accepts a tool call JSON string.
    Validates and executes the tool if allowed.
    Returns the tool result as a string.
    """
    try:
        tool_call = json.loads(tool_call_json)
        tool_name = tool_call.get("tool_call")
        args = tool_call.get("arguments", {})

        if tool_name not in TOOL_FUNCTIONS:
            return f"Error: Tool '{tool_name}' is not allowed."

        func = TOOL_FUNCTIONS[tool_name]

        # validation
        if not isinstance(args, dict):
            return "Invalid arguments format."

        result = func(**args)
        return result

    except Exception as e:
        return f"Tool execution failed: {e}"
