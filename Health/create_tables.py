import sqlite3 
 
conn = sqlite3.connect('status.sqlite') 
 
c = conn.cursor() 
c.execute(''' 
          CREATE TABLE status 
          (id INTEGER PRIMARY KEY ASC,  
           receiver VARCHAR(100) NOT NULL, 
           storage VARCHAR(100) NOT NULL, 
           processing VARCHAR(100), 
           audit VARCHAR(100), 
           last_updated VARCHAR(100) NOT NULL) 
          ''') 
 
conn.commit() 
conn.close()