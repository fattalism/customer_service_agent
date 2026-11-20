import ollama
from app.agent.tools import execute_tool
import json
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tool_definitions import TOOLS
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def call_llm(messages: list):
    return ollama.chat(
        model="qwen3:8b",
        messages=messages,
        tools=TOOLS,
        think=False
    )


def handle_tool_calls(tool_calls, messages):
    for tool in tool_calls:
        tool_name = tool.function.name
        arguments = tool.function.arguments
        call_request = {"name": tool_name, "arguments": arguments}
        try:
            tool_response = execute_tool(call_request)
        except Exception:
            tool_response = {
                "success": False,
                "data": None,
                "error": "Tool execution failed"
            }
            logger.exception("Tool execution failed")
        logger.debug("tool info: %s", tool.model_dump())
        logger.info(
            "Tool execution completed: %s (success=%s)",
            tool_name,
            tool_response.get("success")
        )
        messages.append({"role": "tool", "tool_name": tool_name,
                        "content": json.dumps(tool_response)})


def run_agent(user_message: str):
    messages = [
        SYSTEM_PROMPT,
        {
            "role": "user",
            "content": user_message
        }
    ]

    max_iterations = 5
    for iteration in range(max_iterations):
        logger.info("Agent iteration: %s", iteration + 1)
        try:
            response = call_llm(messages)
        except ollama.RequestError:
            logger.exception("Failed to connect to LLM service")
            return {
                "success": False,
                "data": None,
                "error": "Unable to connect to the LLM service"
            }
        except ollama.ResponseError:
            logger.exception("LLM returned an error")
            return {
                "success": False,
                "data": None,
                "error": "LLM service returned an error"
            }
        logger.info("Tool calls: %s", response.message.tool_calls)
        messages.append(response.message)
        if response.message.tool_calls:
            handle_tool_calls(
                tool_calls=response.message.tool_calls, messages=messages)
        elif not response.message.content:
            return {
                "success": False,
                "data": None,
                "error": "Model returned an empty response"
            }
        else:
            return {
                "success": True,
                "data": {
                    "response": response.message.content
                },
                "error": None
            }

    return {
        "success": False,
        "data": None,
        "error": "Agent reached maximum tool-calling iterations"
    }


response = run_agent(
    "Get the details for orders F1001"
)
print(response)
