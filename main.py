import processing
import pandas as pd

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


data = pd.merge(goldstandard_chunked, goldstandard_alignment, left_index=True, right_index=True).head(5)
print(data)