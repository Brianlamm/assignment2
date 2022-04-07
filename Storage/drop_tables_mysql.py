import mysql.connector 
 
db_conn = mysql.connector.connect(host="acit-3855-lab6.eastus.cloudapp.azure.com", user="", password="", database="events") 
 
db_cursor = db_conn.cursor() 
 
db_cursor.execute(''' 
                  DROP TABLE ticket, sale
                  ''') 
 
db_conn.commit() 
db_conn.close()