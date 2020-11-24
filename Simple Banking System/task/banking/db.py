import sqlite3
from sqlite3 import Error

database = r"card.s3db"


def show_card_balance(number, return_flag):
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT balance FROM card WHERE number=?", (number,))

        rows = cur.fetchall()

        for row in rows:
            if return_flag == 0:
                print(*row)
            else:
                return row[0]


def log_into_account(number, pin):
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT pin FROM card WHERE number=?", (number,))

        rows = cur.fetchall()

        # check correct pin
        for row in rows:
            if row[0] == pin:
                return True
            else:
                return False


def do_transfer(number, number_to_transfer):
    # check correct data transfer
    if number == number_to_transfer:
        print("You can't transfer money to the same account!")
    else:
        # check the Luhn test of credit card numbers
        r = [int(ch) for ch in str(number_to_transfer)][::-1]
        the_Luhn_test = (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0
        if not the_Luhn_test:
            print("Probably you made a mistake in the card number. Please try again!")
        else:
            # check if card not exists
            if not is_card_exist(number_to_transfer):
                print("Such a card does not exist.")
            else:
                # check if there are funds for the balance
                balance = show_card_balance(number, 1)
                transfer_sum = int(input("Enter how much money you want to transfer: "))
                if balance < transfer_sum:
                    print("Not enough money!")
                else:
                    withdraw_money((transfer_sum, number))
                    add_income((transfer_sum, number_to_transfer))


def add_income(transaction):
    """
        update balance via tupple transaction
        :param income:
        :param number:
        """
    conn = create_connection(database)

    sql = ''' UPDATE card
                      SET balance = balance + ?
                      WHERE number = ?'''

    with conn:
        cur = conn.cursor()
        cur.execute(sql, transaction)
    conn.commit()


def withdraw_money(transaction):
    """
    update balance via tupple transaction
    :param transfer_sum:
    :param number_to_transfer:
    """
    conn = create_connection(database)

    sql = ''' UPDATE card
                         SET balance = balance - ?
                         WHERE number = ?'''

    with conn:
        cur = conn.cursor()
        cur.execute(sql, transaction)

    conn.commit()


def is_card_exist(number):
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT number FROM card WHERE number=?)", (number,))

        if cur.fetchone()[0] == 1:
            return True
        else:
            return False


def close_account(number):
    """
        close account via
        :param number:
    """
    conn = create_connection(database)

    sql = 'DELETE FROM card WHERE number=?'

    with conn:
        cur = conn.cursor()
        cur.execute(sql, (number,))
    conn.commit()

    print("The account has been closed!")


def create_connection(path):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(path)
        # print(f"Connection to SQLite DB successful ", sqlite3.version)
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
    Create a new card into the card table
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
