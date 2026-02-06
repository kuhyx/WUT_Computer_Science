import processing
import pandas as pd
import gpt_alignment

# Specify the output file path
file_path = "alignments_with_training_headlines2.wa"

# paths to students andsewrs database
#chunked_path1 = "test_goldStandard/student/STSint.testinput.answers-students.sent1.chunk.txt"
#chunked_path2 = "test_goldStandard/student/STSint.testinput.answers-students.sent2.chunk.txt"
#alignment_path = "test_goldStandard/student/STSint.testinput.answers-students.wa"

# paths to headlines
chunked_path1 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
chunked_path2 = "test_goldStandard/headlines/STSint.testinput.headlines.sent1.chunk.txt"
alignment_path = "test_goldStandard/headlines/STSint.testinput.headlines.wa"

# load data
goldstandard_chunked = processing.load_chunked(chunked_path1, chunked_path2)
goldstandard_alignment = processing.load_alignment(alignment_path)

# get a nice anwser-student table
data = pd.merge(goldstandard_chunked, goldstandard_alignment, left_index=True, right_index=True)
#print(data)

train, test = processing.generate_train_test_split(data)

data_for_chat, indexes = processing.get_chunks_as_text(test)
_, indexes_of_training = processing.get_chunks_as_text(train)
indexes_of_training = [i+1 for i in indexes_of_training]
indexes = [i+1 for i in indexes]
print(indexes_of_training)
print(indexes)

client = gpt_alignment.createGPT()
responses = []
for i in range(0, 10):#len(data_for_chat)):
    responses.append([gpt_alignment.callApi_examples(client, train, data_for_chat[i]), indexes[i]])

with open(file_path, 'w') as file:
    for i, r in enumerate(responses):
        file.write("<sentence id=\"" + str(r[1]+1) + "\" status=\"\">\n")
        file.write("<alignment>\n")
        file.write(r[0])
        file.write("\n</alignment>\n")
        file.write("</sentence>\n\n")