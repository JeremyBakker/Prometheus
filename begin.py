import nltk
from nltk import Text
from textract import process
import io
import re

text = process("Oracle.pdf").decode()
print("type text: ", type(text))
txt = io.StringIO(text)
print("type txt: ", type(txt))
lines = txt.readlines()
print("type lines: ", type(lines))
# print("lines: ", lines)

if "Q\n" in lines:
    # question_matches = [question for question in lines if question == "Q\n"]
    question_indices = [i for i, question in enumerate(lines) if question == "Q\n"]
    # answer_matches = [answer for answer in lines if answer == "A\n"]
    answer_indices = [i for i, answer in enumerate(lines) if answer == 'A\n']
    question_answer_indices = question_indices + answer_indices
    question_answer_indices.sort(key=int)
    print(question_answer_indices)
    print(lines[question_answer_indices[0]-2:question_answer_indices[1]])
    # question_one = lines[(question_indices[0]):]
    # ellipsis_index = [index for index, value in enumerate(question_one) if value.startswith('..........')]
    # print("ellipsis_index[0]: ", ellipsis_index[0])
    # question_one = question_one[0:ellipsis_index[0]]
    # print("question_one: ", question_one)
elif re.search('<Q', str(lines)):
    # question_matches = [question for question in lines if "<Q" in question]
    question_indices = [i for i, question in enumerate(lines) if ("<Q") in question]
    # answer_matches = [question for question in lines if "<A" in question]
    answer_indices = [i for i, question in enumerate(lines) if ("<A") in question]
    question_answer_indices = question_indices + answer_indices
    question_answer_indices.sort(key=int)
    print(question_answer_indices)
    print(lines[question_answer_indices[0]:question_answer_indices[1]])


# print ("question_matches: ", question_matches)
# print("question_matches length: ", len(question_matches))
# print("question_indices: ", question_indices)

# print("answer_matches: ", answer_matches)
# print("answer_matches length: ", len(answer_matches))
# print("answer_indices: ", answer_indices)
