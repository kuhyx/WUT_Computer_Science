import pandas as pd
import processing
import re
import copy

# input file name 
file_path = "alignments_unformatted_headlines.txt"

# output file path
output_file_path = "headlines_fixed_format.wa"

# paths to headlines database
chunked_path1 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
chunked_path2 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
alignment_path = "test_goldStandard/headlines/STSint.testinput.headlines.wa"

# paths to students andsewrs database
#chunked_path1 = "test_goldStandard/student/STSint.testinput.answers-students.sent1.chunk.txt"
#chunked_path2 = "test_goldStandard/student/STSint.testinput.answers-students.sent2.chunk.txt"
#alignment_path = "test_goldStandard/student/STSint.testinput.answers-students.wa"

# load data
goldstandard_chunked = processing.load_chunked(chunked_path1, chunked_path2)
goldstandard_alignment = processing.load_alignment(alignment_path)

# get a nice  table
data = pd.merge(goldstandard_chunked, goldstandard_alignment, left_index=True, right_index=True)

# open generated alignments
with open(file_path, 'r') as file:
    responses = [eval(line.strip()) for line in file.readlines()]

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
    temp = temp.replace("\'", "")
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
    temp = re.sub(r'(^|[^<])(==>+)', r' <==>', temp)
    temp = temp.replace("// - //", "// 0 //")
    temp = temp.replace("// score", "// ")
    temp = temp.replace("// alignment type", "// NOALI")
    temp = temp.replace("> -", "> 0")
    temp = temp.replace("- <", "0 <")
    temp = temp.replace("// //", "// NOALI //")
    temp = temp.replace("equi", "EQUI")
    temp = re.sub(r'\d\. ', '', temp) # remove 1., 2. ...
    temp = temp.upper()
    
    temp = re.sub(r'^(<==>)', r'0 \1', temp)
    temp = re.sub(r'(?<!\n)  +(?!\n)', ' ', temp) # remove double space 

    temp = temp.split("\n")
    for k, t in enumerate(temp):
        if "<==>" not in temp[k]:
            temp[k] = "0 <==> " + temp[k]
        temp[k] = temp[k].split("<==>")
        temp[k] = [temp[k][0], *temp[k][1].split("//")]

        chunk1arr = data.iloc[i]["chunked_sentance1"]
        q = 1
        numberList = []
        for chunk in chunk1arr:
            chunk = re.sub(r'(?<!\n)  +(?!\n)', ' ', chunk)
            n_of_words = len(chunk.strip().split(" "))
            index_str = ""
            for qq in range(q, q + n_of_words):
                index_str =  index_str + str(qq) + " "
            numberList.append(index_str)
            q = q + n_of_words

        for j, chunk in enumerate(data.iloc[i]["chunked_sentance1"]):
            pattern = re.compile(chunk, re.IGNORECASE)
            temp[k][0] = pattern.sub(numberList[j], temp[k][0])

        chunk1arr = data.iloc[i]["chunked_sentance2"]
        q = 1
        numberList = []
        for chunk in chunk1arr:
            chunk = re.sub(r'(?<!\n)  +(?!\n)', ' ', chunk)
            n_of_words = len(chunk.strip().split(" "))
            index_str = ""
            for qq in range(q, q + n_of_words):
                index_str =  index_str + str(qq) + " "
            numberList.append(index_str)
            q = q + n_of_words

        for j, chunk in enumerate(data.iloc[i]["chunked_sentance2"]):
            pattern = re.compile(chunk, re.IGNORECASE)
            temp[k][1] = pattern.sub(numberList[j], temp[k][1])
    
        if any(char.isalpha() and ord(char) < 128 for char in temp[k][0]) or any(char.isalpha() and ord(char) < 128 for char in temp[k][1]):
            temp[k] = ""
        if len(temp[k]) >= 4:
            temp[k][3] = temp[k][3].replace("NOALI", "0")
            if temp[k][3] == "":
                temp[k][3] = " 0 "
            if temp[k][3] == " ":
                temp[k][3] = " 0 "
            temp[k] = temp[k][0] + " <==> " + temp[k][1] + " // " + temp[k][2] + " // " + temp[k][3]
        elif len(temp[k]) == 3:
            temp[k] = temp[k][0] + " <==> " + temp[k][1] + " // " + temp[k][2] + " // 0"    

        temp[k] = re.sub(r'\s{2,}', ' ', temp[k]) # remove double space
    
    temp = [x for x in temp if x != ""]
    responses[i] = "\n".join(temp).strip()

indexes = []
responses_final = []
rejected_indexes = []
for n, r in enumerate(responses):
    if r == '':
        rejected_indexes.append(n+1)
        continue
    if r == '\n':
        rejected_indexes.append(n+1)
        continue
    indexes.append(n+1)
    responses_final.append(r)

print("rejected indexes:")
print(rejected_indexes)

with open(output_file_path, 'w') as file:
    for i, r in zip(indexes, responses_final):
        file.write("<sentence id=\"" + str(i+1) + "\" status=\"\">\n")
        file.write("<alignment>\n")
        file.write(r)
        file.write("\n</alignment>\n")
        file.write("</sentence>\n\n")