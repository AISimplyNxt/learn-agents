"""All model calls go through here. Any OpenAI-compatible server works (Ollama by default)."""
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()


class LLMError(Exception):
    """The model could not be reached, even after retries."""


def chat(messages, tools=None, model=None):
    """Send the messages to the model and return its reply (a plain dict)."""
    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.getenv("LLM_API_KEY", "not-needed-for-local"),
        timeout=float(os.getenv("LLM_TIMEOUT", "120")),
        max_retries=int(os.getenv("LLM_RETRIES", "2")),    # backs off between tries
    )
    options = {"max_tokens": int(os.getenv("LLM_MAX_TOKENS", "512"))}    # a hard cap on each reply
    if os.getenv("LLM_REASONING_EFFORT"):
        options["reasoning_effort"] = os.environ["LLM_REASONING_EFFORT"]
    try:
        response = client.chat.completions.create(
            model=model or os.environ["FAST_MODEL"],
            messages=messages,
            tools=tools or None,
            temperature=0,
            **options,
        )
    except OpenAIError as error:
        raise LLMError(str(error)) from error
    return read_reply(response.choices[0])


def read_reply(choice):
    """A reply cut off by the length cap is a failure, never an answer."""
    if choice.finish_reason == "length":
        raise LLMError("the reply hit the length cap and was cut off")
    return choice.message.model_dump(exclude_none=True)
