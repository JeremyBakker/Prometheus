import sqlite3

with sqlite3.connect('db.sqlite3') as conn:
    c = conn.cursor()
    sql_customer =      ''' CREATE TABLE Answer(
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name            VARCHAR(20) NOT NULL,
                            position        VARCHAR(20) NOT NULL,
                            answer          VARCHAR(100) NOT NULL, 
                            date_of_call    VARCHAR(20) NOT NULL)
                        '''
    c.execute(sql_customer)