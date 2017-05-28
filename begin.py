import nltk
from nltk import Text
from textract import process
import io
import re
import glob

files = glob.glob('AAPL/*.pdf')
for file in files:
    text = process(file).decode()
    txt = io.StringIO(text)
    lines = txt.readlines()
    if "Q\n" in lines:
        question_indices = [i for i, question in enumerate(lines) if question == "Q\n"]
        answer_indices = [i for i, answer in enumerate(lines) if answer == 'A\n']
        question_answer_indices = question_indices + answer_indices
        question_answer_indices.sort(key=int)
        for index, value in enumerate(question_answer_indices):
            print('\n\n')
            print('************************')
            try:
                print(lines[question_answer_indices[index]:question_answer_indices[index+1]])
            except IndexError:
                print(lines[question_answer_indices[index]:])
                print('#######################################################')
                print('NEXT FILE')
                print('#######################################################')
                pass
    elif re.search('<Q', str(lines)):
        question_indices = [i for i, question in enumerate(lines) if ("<Q") in question]
        answer_indices = [i for i, question in enumerate(lines) if ("<A") in question]
        question_answer_indices = question_indices + answer_indices
        question_answer_indices.sort(key=int)
        for index, value in enumerate(question_answer_indices):
            print('\n\n')
            print('************************')
            try:
                print(lines[question_answer_indices[index]:question_answer_indices[index+1]])
            except IndexError:
                print(lines[question_answer_indices[index]:])
                print('#######################################################')
                print('NEXT FILE')
                print('#######################################################')

                pass
    elif re.search('Question[:/-]', str(lines)):
        question_indices = [index for index, question in enumerate(lines) if re.search("Question[:\-]", question)]
        answer_indices = [index for index, question in enumerate(lines) if re.search("Answer[:\-]", question)]
        question_answer_indices = question_indices + answer_indices
        question_answer_indices.sort(key=int)
        for index, value in enumerate(question_answer_indices):
            print('\n\n')
            print('************************')
            try:
                print(lines[question_answer_indices[index]:question_answer_indices[index+1]])
            except IndexError:
                print(lines[question_answer_indices[index]:])
                print('#######################################################')
                print('NEXT FILE')
                print('#######################################################')

                pass