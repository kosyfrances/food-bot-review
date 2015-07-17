import mysql.connector


class CustomSQL(object):
    def __init__(self):
        self.cnx = ""
        self.cursor = ""

    def connect(self):
        self.cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='food_bot_schema')
        self.cursor = self.cnx.cursor()

    def disconnect(self):
        self.cursor.close()
        self.cnx.close()

    def query(self, query_string):
        self.connect()
        self.cursor.execute(query_string)

        result = []
        for row in self.cursor:
            result.append(row)

        self.disconnect()
        return result

query_string = "SELECT * from food_menu"

sql = CustomSQL()
sql.query(query_string)