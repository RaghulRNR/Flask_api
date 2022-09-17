import mysql.connector
try:
    con=mysql.connector.connect(user='root',
                                password='root',
                                host='localhost')
    cur=con.cursor()
    query="CREATE DATABASE gym;"
    cur.execute(query)
    print('Database created successfully')

    query="create table customers (name VARCHAR(255), phoneno VARCHAR(255) );"
    con.commit()
    print('Table created successfully')
except mysql.connector.Error as err:
    con.rollback()
    print('Database Error=', err)
finally:
    if cur:
        cur.close()
    if con:
        con.close()