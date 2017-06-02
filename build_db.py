import sqlite3

with sqlite3.connect('db.sqlite3') as conn:
    c = conn.cursor()
    sql_question_answer =        ''' CREATE TABLE Transcripts(
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name                    VARCHAR(20) NOT NULL,
                            position                VARCHAR(20) NOT NULL,
                            question_answer_text    VARCHAR(100) NOT NULL,
                            question                INTEGER NOT NULL, 
                            date_of_call            VARCHAR(20) NOT NULL)
                        '''
    c.execute(sql_question_answer)