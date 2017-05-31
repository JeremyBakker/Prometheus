import nltk
from nltk import Text
from textract import process
import io
import re
import glob

# Find all the .pdf files
files = glob.glob('Samsung/*.pdf')

for file in files:
    # Convert the text file from pdf and transform it into an iterable list
    text = process(file).decode()
    txt = io.StringIO(text)
    lines = txt.readlines()
    
    # Find where the QUESTION AND ANSWER SECTION begins and ends, then slice it
    # out.
    question_and_answer_section_index = [index for index, item in enumerate(
        lines) if re.search('QUESTION AND ANSWER SECTION\\n', item)]
    disclaimer_index = [index for index, item in enumerate(lines) if re.search(
        'Disclaimer', item)]
    question_and_answer_section = lines[question_and_answer_section_index[0]:
        disclaimer_index[0]]
    
    # Work with files produced from Q3 2011 until the present. The transcript 
    # service marked each question in these files with a capital Q and a new 
    # line.
    if "Q\n" in question_and_answer_section:
        # Find the dots that separate each question/answer block in the file
        # and remove them
        ellipsis_indices = [index for index, ellipsis in enumerate(
            question_and_answer_section) if re.search('.\.\.\.\.\.\.\.\.\.\.+', 
            ellipsis)]
        for index in sorted(ellipsis_indices, reverse=True):
            del question_and_answer_section[index]

        # Find the copyright text at the end of each page and remove it
        copyright_indices = [index for index, copyright_text in enumerate(
            question_and_answer_section) if re.search("|".join(['1-877', 
                '\d{1,2}\\n', 'Copyright', 'LLC', '\\x0c', 
                'Q[0-9] [0-9]{4} Earnings Call', 'Corrected Transcript']), 
                copyright_text)]
        for index in sorted(copyright_indices, reverse=True):
            del question_and_answer_section[index]

        # Find where each question and answer begins in what remains of the 
        # document
        question_indices = [index-3 for index, question in enumerate(
            question_and_answer_section) if question == "Q\n"]
        answer_indices = [index-3 for index, answer in enumerate(
            question_and_answer_section) if answer == 'A\n']
        question_answer_indices = question_indices + answer_indices
        question_answer_indices.sort(key=int)
        question_answer_list = []
        for index, value in enumerate(question_answer_indices):
            try:
                question_answer = question_and_answer_section[
                    question_answer_indices[index]: 
                    question_answer_indices[index + 1]]
            except IndexError:
                question_answer = question_and_answer_section[
                question_answer_indices[index]:]
            question_answer_list.append(question_answer)
        with open("One.txt", "a+") as write_file:
            write_file.write(str(question_answer_list))

    # Work with files from Q1 2005 through Q2 2011 as available. The transcript
    # service marked each question in these files with an angle bracket and a 
    # capital Q.
    elif re.search('<Q', str(lines)):
        pass
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