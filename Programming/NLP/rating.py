#!/usr/bin/env python3
"""Ask the model to rate how similar two chunks are."""

import os

from openai import OpenAI


def _api_key() -> str:
    """Return OPENAI_API_KEY, or explain that it is missing."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        msg = "set OPENAI_API_KEY to run the rating script"
        raise RuntimeError(msg)
    return key


def rate_similarity(c1: list[str], c2: list[str]) -> str:
    """Rate the similarity of two chunk lists on the course's 0-5 scale.

    This was submitted unfinished: it built a client and stopped, so ``c1``
    and ``c2`` were never used and the function returned None despite being
    annotated ``-> str``. The call below is the one the rest of this package
    already makes (see gpt_alignment.call_api); nothing else about the
    original is changed.
    """
    client = OpenAI(api_key=_api_key())
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "user",
                "content": (
                    "Rate on a 0-5 scale how similar these two chunk lists are, "
                    "where 0 is unrelated and 5 is the same meaning. Answer with "
                    "the number alone.\n"
                    f"1: {c1}\n2: {c2}"
                ),
            }
        ],
    )
    return str(response.choices[0].message.content).strip()
