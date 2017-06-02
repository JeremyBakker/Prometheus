import nltk
from nltk import Text
from textract import process
import io
import re
import glob
import sqlite3

# Find all the .pdf files
files = glob.glob('*/*.pdf')

for file in files:
    print(file)
    # Convert the text file from pdf and transform it into an iterable list.
    text = process(file).decode()
    txt = io.StringIO(text)
    lines = txt.readlines()
    
    # Grab the transcript date from the file name for the database entry below.
    transcript_date = str(file[-13:-4])

    # Find where the QUESTION AND ANSWER SECTION begins and ends, then slice it
    # out.
    question_and_answer_section_index = [index for index, item in enumerate(
        lines) if re.search('Q ?UESTION ?-?AND ?-?ANSWER ?-?SECTION\\n', item)]
    disclaimer_index = [index for index, item in enumerate(lines) if re.search(
        'Disclaimer', item)]
    try:
        question_and_answer_section = lines[question_and_answer_section_index[0]:
            disclaimer_index[0]]
    except IndexError:
        question_and_answer_section = lines[407:
            disclaimer_index[0]]

    # # Work with files produced from Q3 2011 until the present. The transcript 
    # # service marked each question in these files with a capital Q and a new 
    # # line.
    if "Q\n" in question_and_answer_section:
        pass
    #     # Find the dots that separate each question/answer block in the file
    #     # and remove them
    #     ellipsis_indices = [index for index, ellipsis in enumerate(
    #         question_and_answer_section) if re.search('.\.\.\.\.\.\.\.\.\.\.+', 
    #         ellipsis)]
    #     for index in sorted(ellipsis_indices, reverse=True):
    #         del question_and_answer_section[index]

    #     # Find the copyright text at the end of each page and remove it
    #     copyright_indices = [index for index, copyright_text in enumerate(
    #         question_and_answer_section) if re.search("|".join(['1-877', 
    #             '\d{1,2}\\n', 'Copyright', '^LLC', '\\x0c', 
    #             'Q[0-9] [0-9]{4} Earnings Call', 'Corrected Transcript']), 
    #             copyright_text)]
    #     for index in sorted(copyright_indices, reverse=True):
    #         del question_and_answer_section[index]

    #     # Remove line breaks
    #     new_line = "\n"
    #     while new_line in question_and_answer_section: \
    #         question_and_answer_section.remove(new_line) 
        
    #     # with open('transcript_no_new.txt', 'a+') as write_file:
    #     #     write_file.write(str(question_and_answer_section))

        # # Find where each question and answer begins in what remains of the 
        # # document
        # question_indices = [index-2 for index, question in enumerate(
        #     question_and_answer_section) if question == "Q\n"]
        # answer_indices = [index-2 for index, answer in enumerate(
        #     question_and_answer_section) if answer == 'A\n']
        # question_answer_indices = question_indices + answer_indices
        # question_answer_indices.sort(key=int)

    #     # Lists to be removed. Here for debugging.
    #     question_list = []
    #     answer_list = []
    #     # Loop through the question and answer section to grab the questions, 
    #     # answers, and conversation partners. Add them to the database.
    #     for index, value in enumerate(question_answer_indices):
    #         try:
    #             question_answer = question_and_answer_section[
    #                 question_answer_indices[index]: 
    #                 question_answer_indices[index + 1]]
    #         except IndexError:
    #             question_answer = question_and_answer_section[
    #             question_answer_indices[index]:]
    #         name = question_answer[0]
    #         position_and_company = question_answer[1]
    #         question_or_answer_text = ''.join(question_answer[3:]).replace(
    #             '\n', '')
    #         if re.search(r'Q\\n', str(question_answer)):
    #             question = True
    #             question_list.append(question_answer)
    #         else:
    #             question = False
    #             answer_list.append(question_answer)
    #         with sqlite3.connect('db.sqlite3') as conn:
    #             c = conn.cursor()
    #             c.execute('''INSERT INTO TRANSCRIPTS VALUES(
    #                 NULL, ?, ?, ?, ?, ?)''', (
    #                     name, 
    #                     position_and_company, 
    #                     question_or_answer_text, 
    #                     question,  
    #                     transcript_date)
    #             )
    #     with open('question.txt', 'a+') as write_file:
    #         write_file.write(str(question_list))
    #     with open('answer.txt', 'a+') as write_file:
    #         write_file.write(str(answer_list))

    # Work with files from Q1 2005 through Q2 2011 as available. The transcript
    # service marked each question in these files with an angle bracket and a 
    # capital Q.
    
    elif re.search('<Q', str(question_and_answer_section)):
        # Find the copyright text at the end of each page and remove it
        copyright_indices = [index for index, copyright_text in enumerate(
            question_and_answer_section) if re.search("|".join(['w ?w ?w ?', 
                '\d{1,2}\\n', 'Company', '^LLC', '\\x0c', 'corrected transcript' 
                'Q[0-9] [0-9]{4} Earnings Call', 'Ticker', 'Event Type', 'Date', 'AAPL', '--']), 
                copyright_text)]
        for index in sorted(copyright_indices, reverse=True):
            del question_and_answer_section[index]

        # Remove line breaks
        new_line = "\n"
        while new_line in question_and_answer_section: \
            question_and_answer_section.remove(new_line)

        # Find where each question and answer begins in what remains of the 
        # document
        question_indices = [index for index, question in enumerate(
            question_and_answer_section) if re.search('<Q', question)]
        answer_indices = [index for index, answer in enumerate(
            question_and_answer_section) if re.search('<A', answer)]
        question_answer_indices = question_indices + answer_indices
        question_answer_indices.sort(key=int)
        
        # Lists to be removed. Here for debugging.
        question_list = []
        answer_list = []
        # Loop through the question and answer section to grab the questions, 
        # answers, and conversation partners. Add them to the database.
        for index, value in enumerate(question_answer_indices):
            try:
                question_answer = question_and_answer_section[
                    question_answer_indices[index]: 
                    question_answer_indices[index + 1]]
            except IndexError:
                question_answer = question_and_answer_section[
                question_answer_indices[index]:]
            colon_index = [index for index, value in enumerate(
                question_answer[0]) if re.search(r':', value)]
            name = question_answer[0][5:colon_index[0]-1]
            position_and_company = False
            question_or_answer_text = ''.join(question_answer)[colon_index[0]+1:
                ].replace('\n', ' ')
            if re.search(r'<Q', str(question_answer)):
                question = True
                question_list.append(question_or_answer_text)
            else:
                question = False
                answer_list.append(question_or_answer_text)
            with sqlite3.connect('db.sqlite3') as conn:
                c = conn.cursor()
                c.execute('''INSERT INTO TRANSCRIPTS VALUES(
                    NULL, ?, ?, ?, ?, ?)''', (
                        name, 
                        position_and_company, 
                        question_or_answer_text, 
                        question,  
                        transcript_date)
                )
        # with open('question.txt', 'a+') as write_file:
        #     write_file.write(str(question_list))
        # with open('answer.txt', 'a+') as write_file:
        #     write_file.write(str(answer_list))

        