import nltk
from nltk import Text
from textract import process
import io
import re
import glob
import sqlite3

# Find all the .pdf files
files = glob.glob('AAPL/*.pdf')

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
        
        # Loop through the question and answer section to grab the questions, 
        # answers, and conversation partners. Put them in a list.
        question_answer_list = []
        question_list = []
        answer_list = []
        for index, value in enumerate(question_answer_indices):
            try:
                question_answer = question_and_answer_section[
                    question_answer_indices[index]: 
                    question_answer_indices[index + 1]]
            except IndexError:
                question_answer = question_and_answer_section[
                question_answer_indices[index]:]
            if re.search(r'Q\\n', str(question_answer)):
                question_list.append(question_answer)
                print("question_answer[0]", type(question_answer[0]))
                print("question_answer[1]", type(question_answer[1]))
                print("question_answer[5:]", type(question_answer[5:]))
                question = ''.join(question_answer[5:]).replace('\n', '')
                print("question", type(question))
                with sqlite3.connect('db.sqlite3') as conn:
                    c = conn.cursor()
                    c.execute('''INSERT INTO ANSWER VALUES(NULL, ?, ?, ?, ?)''', 
                        (question_answer[0], question_answer[1], 
                        question, '2017-05-31'))
            else:
                answer_list.append(question_answer)
        with open('question.txt', 'a+') as write_file:
            write_file.write(str(question_list))
        with open('answer.txt', 'a+') as write_file:
            write_file.write(str(answer_list))

            print("question_answer", question_answer)
            question_answer_list.append(question_answer)
        # with open("One.txt", "a+") as write_file:
        #     write_file.write(str(question_answer_list))

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