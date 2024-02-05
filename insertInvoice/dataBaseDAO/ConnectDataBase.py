import psycopg2


class ConnectDataBase:
    def __init__(self, host, db, usr, pwd):
        try:
            self.connection = psycopg2.connect(
                host=host,
                user=usr,
                password=pwd,
                database=db,
            )
        except psycopg2.OperationalError as e:
            print("Connection failed")
            print(e)
        self.cursor = self.connection.cursor()

    def search(self, sql):
        try:
            cur = self.cursor
            cur.execute(sql)
            rs = cur.fetchall()
        except psycopg2.Error as e:
            return e
        return rs

    def manipulate(self, sql):
        try:
            cur = self.cursor
            cur.execute(sql)
            self.connection.commit()
            if cur.rowcount > 0:
                return print(f'Success insert on db: {sql}')
        except psycopg2.Error as e:
            return e

    def close_connection(self):
        self.cursor.close()
        if self.cursor.close():
            print(f'Finish connection: {self.cursor}, {self.connection}')
