import nltk
from nltk import Text
from textract import process
import io
import re
import glob

files = glob.glob('Microsoft.pdf')
file_count = 0
for file in files:
    text = process(file).decode()
    txt = io.StringIO(text)
    lines = txt.readlines()
    question_indices = [index for index, question in enumerate(lines) if re.search('((<Q)|(Q\\n))|(Question[:-])', question)]
    answer_indices = [index for index, answer in enumerate(lines) if re.search('((<A)|(A\\n))|(Answer[:-])', answer)]
    question_answer_indices = question_indices + answer_indices
    question_answer_indices.sort(key=int)
    for index, value in enumerate(question_answer_indices):
        print('\n\n')
        print('************************')
        try:
            print(lines[question_answer_indices[index]:question_answer_indices[index+1]])
        except IndexError:
            print(lines[question_answer_indices[index]:])
            file_count += 1
            print('#######################################################')
            print('NEXT FILE')
            print('#######################################################')
            pass
print("file_count: ", file_count)
print("question_answer_indices length: ", len(question_answer_indices))