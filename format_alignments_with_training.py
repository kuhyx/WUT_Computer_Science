import pandas as pd
import processing
import re
import copy

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


file_path = "alignments_with_training_student_K.wa"

responses = processing.load_alignment(file_path)
responses = responses["alignment_text"].to_list()


for i, r in enumerate(responses):
    print("\nresponse number " + str(i))
    print(r)

unformatted = copy.deepcopy(responses)

for i, response in enumerate(responses):
    temp = response.lstrip("\n")
    temp = temp.rstrip("\n")

    temp = re.sub(r'(?<==)>', '> ', temp) # add space after >
    temp = re.sub(r'(?<!\n)  +(?!\n)', ' ', temp) # remove double space 

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
    temp = re.sub(r'(^|[^<])(==>+)', r' <==>', temp)
    

    temp = re.sub(r'^(<==>)', r'0 \1', temp)

    temp = re.sub(r'(?<!\n)  +(?!\n)', ' ', temp) # remove double space 

    temp = temp.split("\n")
    for k, t in enumerate(temp):
        temp[k] = temp[k].split("<==>")
        temp[k][1] = temp[k][1].split("//")

        #for j, chunk in enumerate(data.iloc[i]["chunked_sentance1"].sorted(key=len, reverse=True)):
        for j, chunk in enumerate(sorted(data.iloc[i]["chunked_sentance1"], key=lambda x: len(x), reverse=True)):
            pattern = re.compile(chunk, re.IGNORECASE)
            temp[k][0] = pattern.sub(str(j+1), temp[k][0])
            #temp[k][0] = temp[k][0].replace(chunk, str(j+1))
        for j, chunk in enumerate(sorted(data.iloc[i]["chunked_sentance2"], key=lambda x: len(x), reverse=True)):
            pattern = re.compile(chunk, re.IGNORECASE)
            temp[k][1][0] = pattern.sub(str(j+1), temp[k][1][0])
            #temp[k][1][0] = temp[k][1][0].replace(chunk, str(j+1))
        if len(temp[k][1]) >= 3:
            temp[k] = temp[k][0] + " <==> " + temp[k][1][0] + " // " + temp[k][1][1] + " // " + temp[k][1][2]
        elif len(temp[k][1]) == 2:
            temp[k] = temp[k][0] + " <==> " + temp[k][1][0] + " // " + temp[k][1][1] + " // 0"    
        temp[k] = re.sub(r'\s{2,}', ' ', temp[k]) # remove double space
    
    responses[i] = "\n".join(temp)


print("\nafter formatting\n")
for i, r in enumerate(responses):
    print("\nresponse number " + str(i))
    print("FORMATTED\n")
    print(r)
    print("\nUNFORMATTED\n")
    print(unformatted[i])



# write to file 
file_path = "student_fixed_format_with_training.txt"

with open(file_path, 'w') as file:
    for i, r in enumerate(responses):
        file.write("<sentence id=\"" + str(i+1) + "\" status=\"\">\n")
        file.write("<alignment>\n")
        file.write(r)
        file.write("\n</alignment>\n")
        file.write("</sentence>\n\n")