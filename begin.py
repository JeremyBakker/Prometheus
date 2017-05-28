import nltk
from nltk import Text
from textract import process
import io
import re

text = process("Microsoft.pdf").decode()
txt = io.StringIO(text)
lines = txt.readlines()
# print("lines: ", lines)

if "Q\n" in lines:
    question_indices = [i for i, question in enumerate(lines) if question == "Q\n"]
    answer_indices = [i for i, answer in enumerate(lines) if answer == 'A\n']
    question_answer_indices = question_indices + answer_indices
    question_answer_indices.sort(key=int)
    print(question_answer_indices)
    print(lines[question_answer_indices[0]-2:question_answer_indices[1]])
elif re.search('<Q', str(lines)):
    question_indices = [i for i, question in enumerate(lines) if ("<Q") in question]
    answer_indices = [i for i, question in enumerate(lines) if ("<A") in question]
    question_answer_indices = question_indices + answer_indices
    question_answer_indices.sort(key=int)
    print(question_answer_indices)
    print(lines[question_answer_indices[0]:question_answer_indices[1]])
elif re.search('Question[:/-]', str(lines)):
    question_indices = [index for index, question in enumerate(lines) if re.search("Question[:\-]", question)]
    answer_indices = [index for index, question in enumerate(lines) if re.search("Answer[:\-]", question)]
    question_answer_indices = question_indices + answer_indices
    question_answer_indices.sort(key=int)
    print(question_answer_indices)
    print(lines[question_answer_indices[0]:question_answer_indices[1]])