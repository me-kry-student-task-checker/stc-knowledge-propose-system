import sqlite3

def insertMultipleRecords(recordList):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query = """INSERT INTO SqliteDb_calclog
                          (id, numberA, operation, numberB, date) 
                          VALUES (?, ?, ?, ?, ?);"""

        cursor.executemany(sqlite_insert_query, recordList)
        sqliteConnection.commit()
        print("Total", cursor.rowcount, "Records inserted successfully into SqliteDb_calclog table")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert multiple records into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

    recordsToInsert = [(4, '5', '+', '7', '2021-03-18'),
                       (5, '7', '-', '7', '2021-03-18'),
                       (6, '8', '*', '6', '2021-03-18')]

insertMultipleRecords(recordsToInsert)