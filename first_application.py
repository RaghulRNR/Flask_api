import mysql.connector
global cur,con
try:
    con=mysql.connector.connect(user='root',
                                password='root',
                                host='localhost',database='gym')
    cur=con.cursor()
    query="select * from customers"
    result=cur.execute(query)
    print(result)
except mysql.connector.Error as err:
    con.rollback()
    print('Database Error=', err)
finally:
        con.close()
        cur.close()