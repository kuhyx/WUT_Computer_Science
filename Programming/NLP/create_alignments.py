#!/usr/bin/env python3
"""Ask GPT to align the headline chunks, and save the raw replies."""

from pathlib import Path

import gpt_alignment
import pandas as pd
import processing

# Specify the output file path
file_path = "alignments_unformatted_headlines.txt"

# paths to students answers database

# paths to headlines
chunked_path1 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
chunked_path2 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
alignment_path = "test_goldStandard/headlines/STSint.testinput.headlines.wa"

# load data
goldstandard_chunked = processing.load_chunked(chunked_path1, chunked_path2)
goldstandard_alignment = processing.load_alignment(alignment_path)

# get a nice anwser-student table
data = pd.DataFrame.merge(
    goldstandard_chunked, goldstandard_alignment, left_index=True, right_index=True
)

data_for_chat, indexes = processing.get_chunks_as_text(data)

client = gpt_alignment.create_gpt()
responses = [gpt_alignment.call_api(client, chunks) for chunks in data_for_chat]

# Writing to the file with repr() to preserve "\n" characters
with Path(file_path).open("w") as file:
    file.writelines(repr(string) + "\n" for string in responses)
