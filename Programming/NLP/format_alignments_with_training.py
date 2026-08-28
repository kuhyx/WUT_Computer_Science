#!/usr/bin/env python3
"""Format the few-shot alignment replies, and score them against gold."""

import copy
import logging
import re
from pathlib import Path

import pandas as pd
import processing

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.INFO)

# paths to students andsewrs database
student_answers1_path = (
    "test_goldStandard/student/STSint.testinput.answers-students.sent1.txt"
)
student_answers2_path = (
    "test_goldStandard/student/STSint.testinput.answers-students.sent2.txt"
)
student_answers_chunked_path1 = (
    "test_goldStandard/student/STSint.testinput.answers-students.sent1.chunk.txt"
)
student_answers_chunked_path2 = (
    "test_goldStandard/student/STSint.testinput.answers-students.sent2.chunk.txt"
)
student_answers_alignment_path = (
    "test_goldStandard/student/STSint.testinput.answers-students.wa"
)

# load data
student_answers = processing.load_sentences(
    student_answers1_path, student_answers1_path
)
goldstandard_chunked = processing.load_chunked(
    student_answers_chunked_path1, student_answers_chunked_path2
)
goldstandard_alignment = processing.load_alignment(student_answers_alignment_path)

SHORT_FIELDS = 3
MIN_FIELDS = 2

# get a nice anwser-student table
data = pd.DataFrame.merge(
    goldstandard_chunked, goldstandard_alignment, left_index=True, right_index=True
)


file_path = "alignments_with_training_student_K.wa"

responses = processing.load_alignment(file_path)
responses = responses["alignment_text"].to_list()


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
    temp = temp.replace(" ==> ", " <==> ")
    temp = temp.replace(" => ", " <==> ")
    temp = temp.replace(" <=> ", " <==> ")
    temp = temp.replace(" <== ", " <==> ")
    temp = temp.replace("<==> //", " <==> 0 //")
    temp = temp.replace("<==> //", " <==> 0 //")
    temp = temp.replace("NOALI <==>", "0 <==>")
    temp = temp.replace("<==> NOALI", "<==> 0")
    temp = temp.replace("\n// NOALI", "\n0 <==> 0 // NOALI")
    temp = re.sub(r"(^|[^<])(==>+)", r" <==>", temp)

    temp = re.sub(r"^(<==>)", r"0 \1", temp)

    temp = re.sub(r"(?<!\n)  +(?!\n)", " ", temp)  # remove double space

    temp = temp.split("\n")
    for k in range(len(temp)):
        temp[k] = temp[k].split("<==>")
        temp[k][1] = temp[k][1].split("//")

        for j, chunk in enumerate(
            sorted(data.iloc[i]["chunked_sentance1"], key=len, reverse=True)
        ):
            pattern = re.compile(chunk, re.IGNORECASE)
            temp[k][0] = pattern.sub(str(j + 1), temp[k][0])
        for j, chunk in enumerate(
            sorted(data.iloc[i]["chunked_sentance2"], key=len, reverse=True)
        ):
            pattern = re.compile(chunk, re.IGNORECASE)
            temp[k][1][0] = pattern.sub(str(j + 1), temp[k][1][0])
        if len(temp[k][1]) >= SHORT_FIELDS:
            temp[k] = (
                temp[k][0]
                + " <==> "
                + temp[k][1][0]
                + " // "
                + temp[k][1][1]
                + " // "
                + temp[k][1][2]
            )
        elif len(temp[k][1]) == MIN_FIELDS:
            temp[k] = (
                temp[k][0] + " <==> " + temp[k][1][0] + " // " + temp[k][1][1] + " // 0"
            )
        temp[k] = re.sub(r"\s{2,}", " ", temp[k])  # remove double space

    responses[i] = "\n".join(temp)


logger.info("\nafter formatting\n")
for i, r in enumerate(responses):
    logger.info("%s", "\nresponse number " + str(i))
    logger.info("FORMATTED\n")
    logger.info("%s", r)
    logger.info("\nUNFORMATTED\n")
    logger.info("%s", unformatted[i])


# write to file
file_path = "student_fixed_format_with_training.txt"

with Path(file_path).open("w") as file:
    for i, r in enumerate(responses):
        file.write('<sentence id="' + str(i + 1) + '" status="">\n')
        file.write("<alignment>\n")
        file.write(r)
        file.write("\n</alignment>\n")
        file.write("</sentence>\n\n")
