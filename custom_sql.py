import psycopg2
import urlparse


class CustomSQL:
    def __init__(self):
        self.cursor = ""
        self.conn = ""

    def connect(self):
        from config import Config
        config = Config()

        if config["ENVIRONMENT"] == 'production':
            urlparse.uses_netloc.append("postgres")
            url = urlparse.urlparse(config["DATABASE_URL"])
            self.conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )

        else:
            conn_string = "host='localhost' dbname='food_bot'"

            print "Connecting to database\n ->%s" % (conn_string)

            self.conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object
        # you can use this cursor to perform queries
        self.cursor = self.conn.cursor()
        print "Connected!\n"

    def disconnect(self):
        print "Closing connection!\n"
        self.conn.close()

    # def command(self, query_string):
    #     self.connect()
    #     self.cursor.execute(query_string)
    #     self.cursor.execute('commit')
    #     self.disconnect()

    def query(self, query_string, variables):
        self.connect()
        self.cursor.execute(query_string, variables)
        result = []
        for row in self.cursor:
            result.append(row)

        self.disconnect()
        return result
