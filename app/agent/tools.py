from app.clients.oms_client import (
    get_order_details,
    cancel_order,
    create_order
)
import pydantic
from app.schemas import (
    ToolCall,
    GetOrderDetailsArgs,
    CancelOrderArgs,
    CreateOrderRequest)

tool_registry = {
    "get_order_details": {
        "function": get_order_details,
        "schema": GetOrderDetailsArgs
    },
    "cancel_order": {
        "function": cancel_order,
        "schema": CancelOrderArgs
    },
    "create_order": {
        "function": create_order,
        "schema": CreateOrderRequest
    }
}


def execute_tool(response: dict) -> dict:
    try:
        tool_call = ToolCall.model_validate(response)
    except pydantic.ValidationError:
        return {"success": False, "error": "Tool call not parseable"}

    if tool_call.name in tool_registry:
        try:
            tool_def = tool_registry[tool_call.name]['schema'].model_validate(
                tool_call.arguments)
        except pydantic.ValidationError:
            return {"success": False, "error": "Arguments do not match function signature"}

        tool_function = tool_registry[tool_call.name]['function']
        result = tool_function(**tool_def.model_dump())
    else:
        result = {"success": False, "error": "Unknown tool"}
    return result
