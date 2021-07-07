#import mysql.connector
#from mysql.connector import errorcode

# try:
#     conn = mysql.connector.connect(user='root', password='ducanh2001',
#                           host='localhost')
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with your user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)

# cur = conn.cursor()

# cur.execute("CREATE DATABASE IF NOT EXISTS user_portfolio;")
# #cnx.close()



# try:
#     conn = mysql.connector.connect(user='root', password='ducanh2001',
#                           host='localhost', database = 'user_portfolio')
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with your user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)

# cur = conn.cursor(buffered = True)




def create_tables(conn):
    cur = conn.cursor(buffered = True)

    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("DROP TABLE IF EXISTS users")



    query = "CREATE TABLE IF NOT EXISTS transactions"
    create_transaction = query + "(id INT PRIMARY KEY AUTO_INCREMENT, currency_index VARCHAR(7) NOT NULL, status VARCHAR(4) NOT NULL, price FLOAT(6,5), day DATE NOT NULL, volume INT, user_id INT, FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL)"
    query1 = "CREATE TABLE IF NOT EXISTS users"
    create_user = query1 + "(id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(99) UNIQUE NOT NULL, password VARCHAR(99) UNIQUE NOT NULL)"

    cur.execute(create_user)
    cur.execute(create_transaction)


    conn.commit()


def insert_user(conn, username, password):

    cur = conn.cursor(buffered = True)

    query1 = "INSERT INTO users (username, password)"
    query1 = query1 + "VALUES (%s, %s)"


    try:
        cur.execute(query1, (username,password,))
    except Exception as e:
        print(e)

    conn.commit()


def insert_transaction(conn, currency_index, status, price, day, volume, user_id):

    cur = conn.cursor()

    query = "INSERT INTO transactions (currency_index, status, price, day, volume, user_id)"
    query = query + "VALUES (%s, %s, %s, %s, %s, %s)"


    try:
        cur.execute(query, (currency_index, status, price, day, volume, user_id,))
    except Exception as e:
        print(e)

    conn.commit()


