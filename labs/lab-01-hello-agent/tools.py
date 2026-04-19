"""
Tool definitions for lab-01.

Each tool has:
- a JSON schema (sent to the LLM so it knows how to call it)
- a Python handler (what we actually run)
"""
import random

TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Get current weather in Celsius for a city. Returns a mock value for the lab.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, e.g. 'Hanoi'"},
            },
            "required": ["city"],
        },
    },
    {
        "name": "calculator",
        "description": "Evaluate a simple arithmetic expression. Supports + - * / ( ) and decimals.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "e.g. '25 + 10'"},
            },
            "required": ["expression"],
        },
    },
    {
        "name": "return_answer",
        "description": "Call this when you have the final answer for the user. This ends the conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "answer": {"type": "string"},
                "sources": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of tool calls used, e.g. ['get_weather(Hanoi)']",
                },
            },
            "required": ["answer", "sources"],
        },
    },
]


def get_weather(city: str) -> dict:
    # Mock. In real life you would call an API.
    mock_temps = {"hanoi": 25, "saigon": 32, "danang": 28}
    temp = mock_temps.get(city.lower(), random.randint(15, 35))
    return {"city": city, "temp_c": temp, "condition": "sunny"}


def _safe_eval(expr: str) -> float:
    # TODO: replace with a safer parser (ast.parse + whitelist, or `simpleeval`).
    # For the lab, whitelist characters as a minimal guard.
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expr):
        raise ValueError(f"unsafe expression: {expr!r}")
    return eval(expr, {"__builtins__": {}}, {})


def calculator(expression: str) -> dict:
    return {"expression": expression, "result": _safe_eval(expression)}


def return_answer(answer: str, sources: list) -> dict:
    return {"answer": answer, "sources": sources}


TOOL_HANDLERS = {
    "get_weather": get_weather,
    "calculator": calculator,
    "return_answer": return_answer,
}
