#!/usr/bin/env python3
"""Ask GPT to divide the student-answer sentences into iSTS chunks.

The earlier, simpler sibling of ``../gpt_chunks.py``: no format detection and
no reformatting pass, just one request per sentence with the reply written
straight out. Its output is ``chunks_gpt_two.txt`` next to this file.

The prompt lives in ``prompt.txt`` because it is a single 373-character line
that cannot be wrapped without changing the prompt itself.
"""

import logging
import os
from pathlib import Path

from openai import OpenAI

logger = logging.getLogger(__name__)

PROMPT = (Path(__file__).parent / "prompt.txt").read_text(encoding="utf-8").strip()


def sentence_loop(client: OpenAI, sentences: list[str]) -> list[str]:
    """Chunk every sentence, in order, and collect the replies."""
    chunked_sentences: list[str] = []
    for sentence in sentences:
        chunked_sentences = process_sentence(client, sentence, chunked_sentences)
    return chunked_sentences


def process_sentence(
    client: OpenAI, sentence: str, chunked_sentences: list[str]
) -> list[str]:
    """Chunk one sentence and append the reply to *chunked_sentences*."""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": PROMPT + sentence}],
        model="gpt-3.5-turbo",
    )
    chunked_sentence = str(response.choices[0].message.content)
    logger.info("chunked_sentence: %s", chunked_sentence)
    chunked_sentences.append(chunked_sentence)
    return chunked_sentences


def chunk_sentences(file_path: str, output_path: str) -> None:
    """Chunk every sentence in *file_path* and write them to *output_path*."""
    # The key was a literal here with a "Replace me with os.environ" comment
    # next to it, which is now done rather than noted.
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        msg = "set OPENAI_API_KEY to run the chunking script"
        raise RuntimeError(msg)
    client = OpenAI(api_key=key)

    with Path(file_path).open(encoding="utf-8") as file:
        sentences = file.readlines()

    chunked = sentence_loop(client, sentences)
    logger.info("%s", chunked)
    with Path(output_path).open("w", encoding="utf-8") as output_file:
        output_file.writelines(sentence + "\n" for sentence in chunked)


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    chunk_sentences(
        "student/STSint.testinput.answers-students.sent2.txt",
        "chunks_gpt_two.txt",
    )
