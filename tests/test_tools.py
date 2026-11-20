from app.agent.tools import execute_tool
from app.agent.tools import tool_registry


def mock_get_order_details(order_id):
    return {
        "success": True,
        "data": {
            "order_id": order_id,
            "status": "processing"
        },
        "error": None
    }


def test_get_order_details(monkeypatch):
    monkeypatch.setitem(
        tool_registry["get_order_details"],
        "function",
        mock_get_order_details
    )
    result = execute_tool({
        "name": "get_order_details",
        "arguments": {"order_id": "F1001"}
    })

    assert result["data"]["order_id"] == "F1001"
    assert result["data"]["status"] == "processing"


def test_unknown_tool():
    result = execute_tool({
        "name": "unknown_tool",
        "arguments": {}
    })

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Unknown tool"


def test_invalid_arguments():
    result = execute_tool({
        "name": "get_order_details",
        "arguments": {}
    })

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Arguments do not match function signature"


def test_malformed_tool_call():
    result = execute_tool({
        "name": "get_order_details"
    })

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"] == "Tool call not parseable"
