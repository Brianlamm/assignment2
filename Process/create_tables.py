import sqlite3 
 
conn = sqlite3.connect('stats.sqlite') 
 
c = conn.cursor() 
c.execute(''' 
          CREATE TABLE stats 
          (id INTEGER PRIMARY KEY ASC,  
           num_ticket_report INTEGER NOT NULL, 
           num_sale_report INTEGER NOT NULL, 
           min_sale_report INTEGER, 
           max_sale_report INTEGER, 
           last_updated VARCHAR(100) NOT NULL) 
          ''') 
 
conn.commit() 
conn.close()