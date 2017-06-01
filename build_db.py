import sqlite3

with sqlite3.connect('db.sqlite3') as conn:
    c = conn.cursor()
    sql_answer =        ''' CREATE TABLE Answer(
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name            VARCHAR(20) NOT NULL,
                            position        VARCHAR(20) NOT NULL,
                            answer          VARCHAR(100) NOT NULL, 
                            date_of_call    VARCHAR(20) NOT NULL)
                        '''
    sql_question =      ''' CREATE TABLE Question(
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name            VARCHAR(20) NOT NULL,
                            position        VARCHAR(20) NOT NULL,
                            question        VARCHAR(100) NOT NULL, 
                            date_of_call    VARCHAR(20) NOT NULL)
                        '''
    c.execute(sql_answer)
    c.execute(sql_question)