import sqlite3
from sqlite3 import Error


def create_connection(path):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(path)
        print(f"Connection to SQLite DB successful ", sqlite3.version)
    except Error as e:
        print(f"The error '{e}' occurred")

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_card(conn, card):
    """
    Create a new project into the projects table
    :param conn:
    :param card:
    :return: project id
    """
    sql = ''' INSERT INTO card(id,number,pin,balance)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, card)
    conn.commit()
    return cur.lastrowid


def __init_db():
    database = r"card.s3db"

    sql_create_cards_table = """ CREATE TABLE IF NOT EXISTS card (
                                            id INTEGER,
                                            number TEXT,
                                            pin TEXT,
                                            balance INTEGER DEFAULT 0
                                        ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_cards_table)
    else:
        print("Error! cannot create the database connection.")