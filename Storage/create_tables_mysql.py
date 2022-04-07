import mysql.connector 
 
db_conn = mysql.connector.connect(host="acit3855-lab6.westus3.cloudapp.azure.com", user="", password="", database="events") 
 
db_cursor = db_conn.cursor() 
 
db_cursor.execute('''
CREATE TABLE ticket
          (id INT NOT NULL AUTO_INCREMENT, 
           ticket_id VARCHAR(250) NOT NULL,
           date VARCHAR(100) NOT NULL,
           team1 VARCHAR(100) NOT NULL,
           team2 VARCHAR(100) NOT NULL,
           seat_number INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT ticket_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
CREATE TABLE sale
          (id INT NOT NULL AUTO_INCREMENT, 
           sale_id VARCHAR(250) NOT NULL,
           price INTEGER NOT NULL,
           quantity INTEGER NOT NULL,
           trace_id VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT sale_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()