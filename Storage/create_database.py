import sqlite3

conn = sqlite3.connect('reports.sqlite')

c = conn.cursor()
c.execute('''
CREATE TABLE ticket
          (id INTEGER PRIMARY KEY ASC, 
           ticket_id VARCHAR(250) NOT NULL,
           date VARCHAR(100) NOT NULL,
           team1 VARCHAR(100) NOT NULL,
           team2 VARCHAR(100) NOT NULL,
           seat_number INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
CREATE TABLE sale
          (id INTEGER PRIMARY KEY ASC, 
           sale_id VARCHAR(250) NOT NULL,
           price INTEGER NOT NULL,
           quantity INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()