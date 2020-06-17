import sqlite3
import pandas as pd

db_path = 'resources/db.sqlite3'

def create_unique(table, columns, unique):
    '''
    If table does not exist, creates new one with unique columns
    :param table: table name
    :param columns: columns in table
    :param unique: unique columns in table
    :return:
    '''
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    placeholders = ', '.join(columns)
    unique_placeholders = ', '.join(unique)
    qry = "CREATE TABLE IF NOT EXISTS %s ( %s , UNIQUE( %s ) )" % (table, placeholders, unique_placeholders)
    cur.execute(qry)
    cur.close()
    conn.close()

def insert_dict(table, dict_list):
    '''
    Adds each dictionary item to table. Using pandas DF for simplicity, will likely change this once I migrate to MySQL
    :param table: table name
    :param dict_list: list of dictionaries representing a row in the table
    :return:
    '''
    conn = sqlite3.connect(db_path)
    encapsulated = encap_dicts(dict_list)
    for dict in encapsulated:
        #Rows added one at a time so that Integrety Error does not prevent new rows from being added
        row = pd.DataFrame(dict)
        try:
            row.to_sql(table, conn, if_exists="append", index=False)
        except sqlite3.IntegrityError as ex:
            #This error means the row already exists in the table
            continue
    conn.close()

def encap_dicts(dict_list):
    '''
    Puts each dictionary in its own list so they can be added to DataFrames separately
    :param dict_list:
    :return:
    '''
    encapsulated = []
    for dict in dict_list:
        list = []
        list.append(dict)
        encapsulated.append(list.copy())
    return encapsulated

def get_recent(table, columns):
    '''
    Pulls a row from the table and changes its 'posted' column to true
    :param table: table name
    :param columns: columns to return
    :return: A row from the database as a tuple
    '''
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    placeholders = ', '.join(columns)
    sel_qry = "SELECT %s FROM %s WHERE posted=0 ORDER BY date DESC" % (placeholders, table)
    cur.execute(sel_qry)
    rows = cur.fetchone()
    if rows is None:
        return None
    update_qry = 'UPDATE %s SET posted=1 WHERE body=?' % (table)
    cur.execute(update_qry, (rows[2],))
    conn.commit()
    return rows