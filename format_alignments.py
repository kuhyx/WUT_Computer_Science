import pandas as pd
import processing
import re

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


file_path = "alignments_unformatted_student.txt"

# open generated alignments
with open(file_path, 'r') as file:
    responses = [eval(line.strip()) for line in file.readlines()]

for i, r in enumerate(responses):
    print("\nresponse number " + str(i))
    print(r)


for i, response in enumerate(responses):
    temp = response

    temp = re.sub(r'(?<==)>', '> ', temp) # add space after >
    temp = re.sub(r'\s{2,}', ' ', temp) # remove double space 

    temp = temp.replace(" ==> ", " <==> ")
    temp = temp.replace(" <=> ", " <==> ")
    temp = temp.replace(" <== ", " <==> ")
    temp = temp.replace("<==> //", " <==> 0 //")
    temp = temp.replace("<==> //", " <==> 0 //")
    temp = temp.replace("NOALI <==>", "0 <==>")
    temp = temp.replace("<==> NOALI", "<==> 0")

    temp = re.sub(r'^(<==>)', r'0 \1', temp)

    temp = re.sub(r'\s{2,}', ' ', temp) # remove double space 

    #for j, chunk in enumerate(data.iloc[i]["chunked_sentance1"].sorted(key=len, reverse=True)):
    for j, chunk in enumerate(sorted(data.iloc[i]["chunked_sentance1"], key=lambda x: len(x), reverse=True)):
        temp = temp.replace(chunk, str(j+1))
    for j, chunk in enumerate(sorted(data.iloc[i]["chunked_sentance2"], key=lambda x: len(x), reverse=True)):
        temp = temp.replace(chunk, str(j+1))
    
    responses[i] = temp

print("\nafter formatting\n")
for i, r in enumerate(responses):
    print("\nresponse number " + str(i))
    print(r)


# write to file 
file_path = "student_fixed_format.txt"

with open(file_path, 'w') as file:
    for i, r in enumerate(responses):
        file.write("<sentence id=\"" + str(i+1) + "\" status=\"\">\n")
        file.write("<alignment>\n")
        file.write(r)
        file.write("</alignment>\n")
        file.write("</sentence>\n")