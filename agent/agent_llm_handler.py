import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agent.tool_executor import execute_tool_call

#environment variables
load_dotenv()

#Ollama & OpenAI client
client = AsyncOpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    api_key="ollama"
)

# System prompt
SYSTEM_PROMPT = """
You are a helpful assistant that can access tools to answer user queries.
Only use tools when necessary. Tools should be called in the following JSON format:

{
  "tool_call": "tool_name",
  "arguments": {
    "arg1": "value1",
    "arg2": "value2"
  }
}

If no tool is needed, respond naturally. If you use a tool, return only the JSON.
"""

async def run_agent_chain(user_query: str) -> str:
    """
    Given a user query, this function routes it through the agentic workflow:
    1. Ask the LLM if it wants to use a tool.
    2. If yes, parse and run the tool.
    3. Feed the tool's output back to the LLM.
    4. Return the final natural language answer.
    """
    try:
        # First call: Ask the LLM how to respond to the user
        initial_response = await client.chat.completions.create(
            model="qwen:0.5b",  # alternative qwen:1b
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
        )

        assistant_message = initial_response.choices[0].message.content.strip()

        # Try to parse the response as a tool call
        try:
            tool_request = json.loads(assistant_message)

            if isinstance(tool_request, dict) and "tool_call" in tool_request:
                # It's a tool request – run the corresponding function
                tool_output = execute_tool_call(json.dumps(tool_request))

                # Second call: Pass tool result to LLM for final summary
                final_response = await client.chat.completions.create(
                    model="qwen:0.5b",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_query},
                        {"role": "assistant", "content": assistant_message},
                        {"role": "function", "content": tool_output}
                    ]
                )

                return final_response.choices[0].message.content.strip()

            else:
                # No tool needed, return assistant's direct answer
                return assistant_message

        except json.JSONDecodeError:
            # Assistant gave a natural answer, not a tool call
            return assistant_message

    except Exception as error:
        return f"Agent failed with error: {str(error)}"

#debugging
if __name__ == "__main__":
    import asyncio
    async def test():
        query = "What are the latest PIB updates about agriculture?"
        response = await run_agent_chain(query)
        print(f"\n🔍 Agent Response:\n{response}\n")

    asyncio.run(test())
