#!/usr/bin/env python3
"""Get chunk alignment from ChatGPT.

The two prompts live in ``prompts/`` rather than in this file: they are 2 kB
of instructions each, on lines far past any line-length limit, and wrapping
them here would put newlines into the middle of the prompt itself.
"""

import os
from pathlib import Path

import pandas as pd
from openai import OpenAI

PROMPTS = Path(__file__).parent / "prompts"
THE_PROMPT = (PROMPTS / "alignment.txt").read_text(encoding="utf-8")
THE_PROMPT_WITH_COMMENT = (PROMPTS / "alignment_with_comment.txt").read_text(
    encoding="utf-8"
)


def create_gpt() -> OpenAI:
    """Build an OpenAI client from OPENAI_API_KEY.

    The key used to be a placeholder string literal here, which meant the
    script could not actually run as committed.
    """
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        msg = "set OPENAI_API_KEY to run the alignment scripts"
        raise RuntimeError(msg)
    return OpenAI(api_key=key)


def call_api(client: OpenAI, chunks: str) -> str:
    """Ask the model to align one pair of chunked sentences."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "user", "content": THE_PROMPT},
            {"role": "user", "content": chunks},
        ],
    )
    return response.choices[0].message.content.strip()


def call_api_examples(client: OpenAI, examples: pd.DataFrame, alignment: str) -> str:
    """Ask the model to align, few-shot prompted with worked examples."""
    user_input = []
    assistant_output = []
    for _index, row in examples.iterrows():
        chunks = ""
        for chunk in row["chunked_sentance1"]:
            chunks = chunks + "[ " + chunk + " ] "
        chunks = chunks + "\n"
        for chunk in row["chunked_sentance2"]:
            chunks = chunks + "[ " + chunk + " ] "
        user_input.append(chunks)
        assistant_output.append(row["alignment_text"])

    messages = []
    messages.append({"role": "user", "content": THE_PROMPT})
    for u, a in zip(user_input, assistant_output, strict=True):
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})

    messages.append({"role": "user", "content": alignment})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", messages=messages
    )
    return response.choices[0].message.content.strip()
