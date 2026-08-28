#!/usr/bin/env python3
"""Turn the raw GPT alignment replies into the SemEval .wa format."""

import ast
import copy
import logging
import re
from pathlib import Path

import pandas as pd
import processing

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.INFO)

# input file name
file_path = "alignments_unformatted_headlines.txt"

# output file path
output_file_path = "headlines_fixed_format.wa"

# paths to headlines database
chunked_path1 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
chunked_path2 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
alignment_path = "test_goldStandard/headlines/STSint.testinput.headlines.wa"

# paths to students andsewrs database

# load data
goldstandard_chunked = processing.load_chunked(chunked_path1, chunked_path2)
goldstandard_alignment = processing.load_alignment(alignment_path)

# ASCII letters mark a chunk the numbering pass failed to replace, and a
# formatted alignment always has at least the four //-separated fields.
ASCII_MAX = 128
FULL_FIELDS = 4
SHORT_FIELDS = 3

# get a nice  table
data = pd.DataFrame.merge(
    goldstandard_chunked, goldstandard_alignment, left_index=True, right_index=True
)

# open generated alignments
# The file holds one repr()'d string per line (see create_alignments.py),
# so literal_eval is enough -- eval() here would execute whatever GPT
# happened to return.
with Path(file_path).open() as file:
    responses = [ast.literal_eval(line.strip()) for line in file]

for i, r in enumerate(responses):
    logger.info("%s", "\nresponse number " + str(i))
    logger.info("%s", r)

unformatted = copy.deepcopy(responses)

for i, response in enumerate(responses):
    temp = response.lstrip("\n")
    temp = temp.rstrip("\n")

    temp = re.sub(r"(?<==)>", "> ", temp)  # add space after >
    temp = re.sub(r"(?<!\n)  +(?!\n)", " ", temp)  # remove double space

    temp = temp.replace("]", "")
    temp = temp.replace("[", "")
    temp = temp.replace("'", "")
    temp = temp.replace(" ==> ", " <==> ")
    temp = temp.replace(" => ", " <==> ")
    temp = temp.replace(" <=> ", " <==> ")
    temp = temp.replace(" <== ", " <==> ")
    temp = temp.replace("<==> //", " <==> 0 //")
    temp = temp.replace("NOALI <==>", "0 <==>")
    temp = temp.replace("<==> NOALI", "<==> 0")
    temp = temp.replace("\n// NOALI", "\n0 <==> 0 // NOALI")
    temp = temp.replace("\n // ", "\n0 <==> ")
    temp = temp.replace("\n// ", "\n0 <==> ")
    temp = re.sub(r"(^|[^<])(==>+)", r" <==>", temp)
    temp = temp.replace("// - //", "// 0 //")
    temp = temp.replace("// score", "// ")
    temp = temp.replace("// alignment type", "// NOALI")
    temp = temp.replace("> -", "> 0")
    temp = temp.replace("- <", "0 <")
    temp = temp.replace("// //", "// NOALI //")
    temp = temp.replace("equi", "EQUI")
    temp = re.sub(r"\d\. ", "", temp)  # remove 1., 2. ...
    temp = temp.upper()

    temp = re.sub(r"^(<==>)", r"0 \1", temp)
    temp = re.sub(r"(?<!\n)  +(?!\n)", " ", temp)  # remove double space

    temp = temp.split("\n")
    for k, t in enumerate(temp):
        if "<==>" not in t:
            temp[k] = "0 <==> " + temp[k]
        temp[k] = temp[k].split("<==>")
        temp[k] = [temp[k][0], *temp[k][1].split("//")]

        chunk1arr = data.iloc[i]["chunked_sentance1"]
        q = 1
        number_list = []
        for raw_chunk in chunk1arr:
            chunk = re.sub(r"(?<!\n)  +(?!\n)", " ", raw_chunk)
            n_of_words = len(chunk.strip().split(" "))
            index_str = ""
            for qq in range(q, q + n_of_words):
                index_str = index_str + str(qq) + " "
            number_list.append(index_str)
            q = q + n_of_words

        for j, chunk in enumerate(data.iloc[i]["chunked_sentance1"]):
            pattern = re.compile(chunk, re.IGNORECASE)
            temp[k][0] = pattern.sub(number_list[j], temp[k][0])

        chunk1arr = data.iloc[i]["chunked_sentance2"]
        q = 1
        number_list = []
        for raw_chunk in chunk1arr:
            chunk = re.sub(r"(?<!\n)  +(?!\n)", " ", raw_chunk)
            n_of_words = len(chunk.strip().split(" "))
            index_str = ""
            for qq in range(q, q + n_of_words):
                index_str = index_str + str(qq) + " "
            number_list.append(index_str)
            q = q + n_of_words

        for j, chunk in enumerate(data.iloc[i]["chunked_sentance2"]):
            pattern = re.compile(chunk, re.IGNORECASE)
            temp[k][1] = pattern.sub(number_list[j], temp[k][1])

        if any(char.isalpha() and ord(char) < ASCII_MAX for char in temp[k][0]) or any(
            char.isalpha() and ord(char) < ASCII_MAX for char in temp[k][1]
        ):
            temp[k] = ""
        if len(temp[k]) >= FULL_FIELDS:
            temp[k][3] = temp[k][3].replace("NOALI", "0")
            if temp[k][3] == "":
                temp[k][3] = " 0 "
            if temp[k][3] == " ":
                temp[k][3] = " 0 "
            temp[k] = (
                temp[k][0]
                + " <==> "
                + temp[k][1]
                + " // "
                + temp[k][2]
                + " // "
                + temp[k][3]
            )
        elif len(temp[k]) == SHORT_FIELDS:
            temp[k] = temp[k][0] + " <==> " + temp[k][1] + " // " + temp[k][2] + " // 0"

        temp[k] = re.sub(r"\s{2,}", " ", temp[k])  # remove double space

    temp = [x for x in temp if x != ""]
    responses[i] = "\n".join(temp).strip()

indexes = []
responses_final = []
rejected_indexes = []
for n, r in enumerate(responses):
    if r == "":
        rejected_indexes.append(n + 1)
        continue
    if r == "\n":
        rejected_indexes.append(n + 1)
        continue
    indexes.append(n + 1)
    responses_final.append(r)

logger.info("rejected indexes:")
logger.info("%s", rejected_indexes)

with Path(output_file_path).open("w") as file:
    for i, r in zip(indexes, responses_final, strict=False):
        file.write('<sentence id="' + str(i + 1) + '" status="">\n')
        file.write("<alignment>\n")
        file.write(r)
        file.write("\n</alignment>\n")
        file.write("</sentence>\n\n")
