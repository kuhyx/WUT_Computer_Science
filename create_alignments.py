import processing
import pandas as pd
import gpt_alignment

# paths to students andsewrs database
studentAnswers1_path = "test_goldStandard/student/STSint.testinput.answers-students.sent1.txt"
studentAnswers2_path = "test_goldStandard/student/STSint.testinput.answers-students.sent2.txt"
studentAnsewrs_chunked_path1 = "test_goldStandard/student/STSint.testinput.answers-students.sent1.chunk.txt"
studentAnsewrs_chunked_path2 = "test_goldStandard/student/STSint.testinput.answers-students.sent2.chunk.txt"
studentsAnsewrs_alignment_path = "test_goldStandard/student/STSint.testinput.answers-students.wa"

# load data
studentAnserws = processing.load_sentences(studentAnswers1_path, studentAnswers1_path)
goldstandard_chunked = processing.load_chunked(studentAnsewrs_chunked_path1, studentAnsewrs_chunked_path2)
goldstandard_alignment = processing.load_alignment(studentsAnsewrs_alignment_path)

# get a nice anwser-student table
data = pd.merge(goldstandard_chunked, goldstandard_alignment, left_index=True, right_index=True)
print(data)

data_for_chat = processing.get_chunks_as_text(data)

# generate a few examples
#for i in range(1, 10):
#    print(processing.generate_alignment_format(data, i))
#    print("correct anwser for this is: ")
#    print(data["alignment_text"][i])
# best prompt so far

client = gpt_alignment.createGPT()
responses = []
for i in range(0, len(data_for_chat)):
    responses.append(gpt_alignment.callApi(client, data_for_chat[i]))
    
# Specify the file path
file_path = "alignments_unformatted_student.txt"

# Writing to the file with repr() to preserve "\n" characters
with open(file_path, 'w') as file:
    for string in responses:
        file.write(repr(string) + '\n')