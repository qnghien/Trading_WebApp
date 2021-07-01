import mysql.connector
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

    cur.execute("DROP TABLE IF EXISTS transaction")
    cur.execute("DROP TABLE IF EXISTS user")



    query = "CREATE TABLE IF NOT EXISTS transaction"
    create_transaction = query + "(id INT PRIMARY KEY AUTO_INCREMENT, currency_index VARCHAR(7) NOT NULL, status VARCHAR(4) NOT NULL, price FLOAT(6,5), day DATE NOT NULL, volume INT, user_id INT, FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL)"
    query1 = "CREATE TABLE IF NOT EXISTS user"
    create_user = query1 + "(id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(99) UNIQUE NOT NULL, password VARCHAR(99) UNIQUE NOT NULL)"

    cur.execute(create_user)
    cur.execute(create_transaction)


    conn.commit()


def insert_user(conn, username, password):

    cur = conn.cursor(buffered = True)

    query1 = "INSERT INTO user (username, password)"
    query1 = query1 + "VALUES (%s, %s)"


    try:
        cur.execute(query1, (username,password,))
    except Exception as e:
        print(e)

    conn.commit()


def insert_transaction(conn, currency_index, status, price, day, volume, user_id):

    cur = conn.cursor()

    query = "INSERT INTO transaction (currency_index, status, price, day, volume, user_id)"
    query = query + "VALUES (%s, %s, %s, %s, %s, %s)"


    try:
        cur.execute(query, (currency_index, status, price, day, volume, user_id,))
    except Exception as e:
        print(e)

    conn.commit()


def valid_login(conn, username, password):

    cur = conn.cursor(buffered = True)

    query_username = "SELECT username FROM user"

    cur.execute(query_username)
    username_list = []

    try:
        rows = cur.fetchall()
        for row in rows:
            username_list.append(row[0])

    except mysql.connector.errors.InterfaceError as ie:
        if ie.msg == 'No result set to fetch from.':
            print("Empty set")
        else:
            raise

    query_password = "SELECT password FROM user \
                        WHERE username = ?"

    if username not in username_list:
        print("Username has not been signed up !")
        return False
    else:
        cur.execute(query_password, (username,))
        try:
            row = cur.fetchone()
            if password != row[0]:
                print("Invalid Login")
            else:
                return True
        except mysql.connector.errors.InterfaceError as ie:
            if ie.msg == 'No result set to fetch from.':
                print("Empty set")
            else:
                raise


