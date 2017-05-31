import nltk
from nltk import Text
from textract import process
import io
import re
import glob

files = glob.glob('Oracle/*.pdf')
for file in files:
    # Convert the text file from pdf and transform it into an iterable list
    text = process(file).decode()
    txt = io.StringIO(text)
    lines = txt.readlines()
    
    # Find where the QUESTION AND ANSWER SECTION begins and ends, then slice it
    # out
    question_and_answer_section_index = [index for index, item in enumerate(
        lines) if re.search('QUESTION AND ANSWER SECTION\\n', item)]
    disclaimer_index = [index for index, item in enumerate(lines) if re.search('Disclaimer', item)]
    question_and_answer_section = lines[question_and_answer_section_index[0]:
        disclaimer_index[0]]
    
    if "Q\n" in lines:
        pass
        # Work with files produced from Q3 2011 until the present
        # The transcript service marked each question with a capital Q and a 
        # new line
        # with open("One.txt", "a+") as write_file:
        #     write_file.write(''.join(lines))
        # question_indices = [i for i, question in enumerate(lines) if question == "Q\n"]
        # answer_indices = [i for i, answer in enumerate(lines) if answer == 'A\n']
        # question_answer_indices = question_indices + answer_indices
        # question_answer_indices.sort(key=int)
        # for index, value in enumerate(question_answer_indices):
        #     print('\n\n')
        #     print('************************')
        #     try:
        #         print(lines[question_answer_indices[index]:question_answer_indices[index+1]])
        #     except IndexError:
        #         print(lines[question_answer_indices[index]:])
        #         print('#######################################################')
        #         print('NEXT FILE')
        #         print('#######################################################')
        #         pass
    elif re.search('<Q', str(lines)):
        pass
        # Work with files from Q1 2005 through Q2 2011 as available
        # The transcript service marked each question with an angle bracket and
        # a capital Q
        # with open("Two.txt", "a+") as write_file:
        #     write_file.write(''.join(lines))
        # question_indices = [i for i, question in enumerate(lines) if ("<Q") in question]
        # answer_indices = [i for i, question in enumerate(lines) if ("<A") in question]
        # question_answer_indices = question_indices + answer_indices
        # question_answer_indices.sort(key=int)
        # for index, value in enumerate(question_answer_indices):
        #     print('\n\n')
        #     print('************************')
        #     try:
        #         print(lines[question_answer_indices[index]:question_answer_indices[index+1]])
        #     except IndexError:
        #         print(lines[question_answer_indices[index]:])
        #         print('#######################################################')
        #         print('NEXT FILE')
        #         print('#######################################################')
        #         pass