import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="calculatoruser",
    password="calculatorpw",
    database="calculator"
)
cursor = db.cursor()


def insert_result(numberA, numberB, operation, result):
    statement = "INSERT INTO calculations (numberA, numberB, operation, result) values (%s,%s,%s,%s)"
    values = (numberA, numberB, operation, result)
    cursor.execute(statement, values)
    db.commit()


def get_calculations():
    statement = "SELECT * FROM calculations"
    cursor.execute(statement)
    return cursor.fetchall()


