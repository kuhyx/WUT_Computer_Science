#!/usr/bin/env python3
"""Ask GPT to align chunks, few-shot prompted with gold examples."""

import logging
from pathlib import Path

import gpt_alignment
import pandas as pd
import processing

logger = logging.getLogger(__name__)

# Specify the output file path
file_path = "alignments_with_training_headlines2.wa"

# paths to students andsewrs database

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

train, test = processing.generate_train_test_split(data)

data_for_chat, indexes = processing.get_chunks_as_text(test)
_, indexes_of_training = processing.get_chunks_as_text(train)
indexes_of_training = [i + 1 for i in indexes_of_training]
indexes = [i + 1 for i in indexes]
logger.info("%s", indexes_of_training)
logger.info("%s", indexes)

client = gpt_alignment.create_gpt()
# Ten only: each call is a paid few-shot request, and ten was enough for the
# report's comparison.
SAMPLE_SIZE = 10
responses = [
    [gpt_alignment.call_api_examples(client, train, data_for_chat[i]), indexes[i]]
    for i in range(SAMPLE_SIZE)
]

with Path(file_path).open("w") as file:
    for r in responses:
        file.write('<sentence id="' + str(r[1] + 1) + '" status="">\n')
        file.write("<alignment>\n")
        file.write(r[0])
        file.write("\n</alignment>\n")
        file.write("</sentence>\n\n")
