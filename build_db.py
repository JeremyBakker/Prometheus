import sqlite3
import glob

files = glob.glob('Data/*/*.pdf')

corporation_set = set()

for file in files:
    
    # Grab the stock symbol from the file name for use below in the SQL insert
    # statements. Each stock symbol is preceded by an opening parenthesis and 
    # ends with a hyphen in the file name.
    parenthesis_index = file.index('(')
    hyphen_index = file.index('-')
    corporation = file[parenthesis_index+1:hyphen_index]

    corporation_set.add(corporation)


for corporation in corporation_set:
    print(corporation)
    with sqlite3.connect('db.sqlite3') as conn:
        c = conn.cursor()
        sql_question_answer =   ''' CREATE TABLE {}(
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                corporation             VARCHAR(20) NOT NULL,
                                name                    VARCHAR(20) NOT NULL,
                                question_answer_text    VARCHAR(100) NOT NULL,
                                question                INTEGER NOT NULL, 
                                date_of_call            DATE NOT NULL)
                                '''.format(corporation)
        c.execute(sql_question_answer)