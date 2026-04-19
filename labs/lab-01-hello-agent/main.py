"""
Lab 01 - Hello Agent (skeleton).

Your job: fill in the agent loop so the script can answer a question by
calling tools iteratively.

Run:
    python main.py "What is the weather in Hanoi plus 10 degrees?"
"""
import os
import sys
import json
from anthropic import Anthropic
from dotenv import load_dotenv

from tools import TOOL_SCHEMAS, TOOL_HANDLERS

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_ITERS = 10
SYSTEM = (
    "You are a helpful agent. Use tools to answer the user. "
    "When you have the final answer, call `return_answer` with a short "
    "`answer` string and a `sources` list of tool calls you used."
)


def run_agent(user_input: str) -> dict:
    client = Anthropic()
    messages = [{"role": "user", "content": user_input}]

    for step in range(MAX_ITERS):
        # TODO (1): call client.messages.create with model, max_tokens,
        # system=SYSTEM, tools=TOOL_SCHEMAS, messages=messages.
        response = ...

        # TODO (2): if response.stop_reason == "end_turn", parse the final
        # return_answer tool call (it should be the last tool_use in content)
        # and return its input as dict.

        # TODO (3): if response.stop_reason == "tool_use", iterate over
        # content blocks. For each tool_use block:
        #   - print "[tool] name(input)" for visibility
        #   - run TOOL_HANDLERS[name](**input)
        #   - collect a tool_result block with tool_use_id + content
        # Then append:
        #   messages.append({"role": "assistant", "content": response.content})
        #   messages.append({"role": "user", "content": tool_results})
        # and continue the loop.

        raise NotImplementedError("fill the TODOs above")

    raise RuntimeError(f"Agent did not finish in {MAX_ITERS} iterations")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'your question'")
        sys.exit(1)
    result = run_agent(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
