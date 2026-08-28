#!/usr/bin/env python3
"""Compare kuhy's GPT chunkings against the SemEval gold standard.

Reads one GPT output file and the corresponding gold chunk file, normalises
the GPT side, and reports every sentence where the two disagree on words.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def reformat_sentence(sentence: str) -> str:
    """Reformats a sentence by replacing slashes '/' with ' ]'."""
    return sentence.replace("/", " ]")


def insert_commas(sentence: str, reference_sentence: str) -> str:
    """Insert commas into *sentence* where *reference_sentence* has them."""
    # Splitting the sentences into chunks
    sentence_chunks = sentence.split(" ] [ ")
    reference_chunks = reference_sentence.split(" ] [ ")

    # Insert commas into the original sentence based on the reference sentence
    for i, chunk in enumerate(reference_chunks):
        if "," in chunk and i < len(sentence_chunks):
            sentence_chunks[i] += ","

    # Reconstruct the sentence with inserted commas
    return " ] [ ".join(sentence_chunks)


def process_sentences(
    sentences1: list[str], sentences2: list[str]
) -> list[dict[str, object]]:
    """Compare each GPT chunking against its gold counterpart."""
    processed_sentences = []

    for sentence1, sentence2 in zip(sentences1, sentences2, strict=False):
        # Reformat the first sentence
        reformatted_sentence1 = reformat_sentence(sentence1)
        reformatted_sentence1 = insert_commas(reformatted_sentence1, sentence2)
        # Splitting the sentences into words, ignoring the square brackets
        words1 = set(
            " ".join(reformatted_sentence1.strip().split("] ["))
            .replace("[", "")
            .replace("]", "")
            .lower()
            .split()
        )
        words2 = set(
            " ".join(sentence2.strip().split("] ["))
            .replace("[", "")
            .replace("]", "")
            .lower()
            .split()
        )

        # Finding differences in words
        diff = words2 - words1

        # Preparing the output sentence
        output_sentence = reformatted_sentence1.strip()
        if "[ . ]" in sentence2:
            output_sentence += " [ . ]"

        # Record the differences alongside the merged sentence.
        processed_sentences.append(
            {
                "sentence1": reformatted_sentence1.strip(),
                "sentence2": sentence2.strip(),
                "differences": diff,
                "merged_sentence": output_sentence,
            }
        )
        if diff and diff != {"."}:
            logger.info("Difference found!")
            logger.info("Sentence 1: %s", reformatted_sentence1.strip())
            logger.info("Sentence 2: %s", sentence2.strip())
            logger.info("Differences: %s", diff)
            logger.info("\n")

    return processed_sentences


# The GPT output and the gold chunking for the same corpus half.
file_path_1 = "test_goldStandard/images/images-chunks-gpt-one.txt"
file_path_2 = "test_goldStandard/images/STSint.testinput.images.sent1.chunk.txt"

# Reading the files
with Path(file_path_1).open() as file1, Path(file_path_2).open() as file2:
    sentences_file_1 = file1.readlines()
    sentences_file_2 = file2.readlines()

# Process the sentences
processed_sentences = process_sentences(sentences_file_1, sentences_file_2)
