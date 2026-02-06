import processing
import pandas as pd
import gpt_alignment

# Specify the output file path
file_path = "alignments_unformatted_headlines.txt"

# paths to students answers database
#chunked_path1 = "test_goldStandard/student/STSint.testinput.answers-students.sent1.chunk.txt"
#chunked_path2 = "test_goldStandard/student/STSint.testinput.answers-students.sent2.chunk.txt"
#alignment_path = "test_goldStandard/student/STSint.testinput.answers-students.wa"

# paths to headlines
chunked_path1 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
chunked_path2 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
alignment_path = "test_goldStandard/headlines/STSint.testinput.headlines.wa"

# load data
#studentAnserws = processing.load_sentences(studentAnswers1_path, studentAnswers1_path)
goldstandard_chunked = processing.load_chunked(chunked_path1, chunked_path2)
goldstandard_alignment = processing.load_alignment(alignment_path)

# get a nice anwser-student table
data = pd.merge(goldstandard_chunked, goldstandard_alignment, left_index=True, right_index=True)
#print(data)

data_for_chat, indexes = processing.get_chunks_as_text(data)

client = gpt_alignment.createGPT()
responses = []
for i in range(0, len(data_for_chat)):
    responses.append(gpt_alignment.callApi(client, data_for_chat[i]))

# Writing to the file with repr() to preserve "\n" characters
with open(file_path, 'w') as file:
    for string in responses:
        file.write(repr(string) + '\n')