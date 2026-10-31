import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.llm import LLMError, read_reply


def choice(finish_reason):
    message = SimpleNamespace(model_dump=lambda exclude_none: {"role": "assistant", "content": "Hi"})
    return SimpleNamespace(finish_reason=finish_reason, message=message)


def test_finished_reply_is_returned():
    assert read_reply(choice("stop"))["content"] == "Hi"


def test_cut_off_reply_is_a_failure():
    with pytest.raises(LLMError):
        read_reply(choice("length"))
