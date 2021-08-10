#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('BCIE.db')
print("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE BCIE
       (ID INTEGER PRIMARY KEY autoincrement,
       UID INTEGER UNIQUE NOT NULL,
       TIME TIMESTAMP default (datetime('now', 'localtime')));
      ''')

c.execute('''CREATE INDEX index_uid
 on BCIE (UID);''')
print("Table created successfully")
conn.commit()
conn.close()