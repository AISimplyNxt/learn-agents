"""A scripted fake model, so tests pass without any model running."""
import json


def tool_call(name, call_id="call_1", **arguments):
    """A reply that asks our code to run a tool."""
    return {
        "role": "assistant",
        "tool_calls": [{
            "id": call_id,
            "type": "function",
            "function": {"name": name, "arguments": json.dumps(arguments)},
        }],
    }


def answer(text):
    """A reply that finishes the job."""
    return {"role": "assistant", "content": text}


class FakeLLM:
    """Plays back its replies in order, and remembers what it was sent."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.seen = []

    def __call__(self, messages, tools=None, model=None):
        self.seen.append([dict(m) for m in messages])
        return self.replies.pop(0)
