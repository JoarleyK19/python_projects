import json
import os

from dataBaseDAO.ConnectDataBase import ConnectDataBase


class OpenDataBase:
    def __init__(self, db_json: str):
        self._db_json: str = db_json
        self.__conn = None
        self.__host = None
        self.__database = None
        self.__user = None
        self.__password = None

    @property
    def db_json(self):
        return self._db_json

    @db_json.setter
    def db_json(self, new_db_json):
        self._db_json = new_db_json

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, new_conn):
        self.__conn = new_conn

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, new_host):
        self.__host = new_host

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, new_database):
        self.__database = new_database

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, new_user):
        self.__user = new_user

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        self.__password = new_password

    def open_json(self):
        data_base = None
        name_json = self.db_json
        dirlist = os.listdir("./model")
        for i in dirlist:
            filename = os.path.join("model/")
            full_path = os.path.abspath(filename + i)
            if name_json in full_path:
                with open(full_path, encoding='utf-8') as json_path:
                    data_base = json.load(json_path)
        return data_base

    def view_data_base(self):
        db = self.open_json()
        list_db = []
        if db is not None:
            for i in db:
                list_db.append(i['name'].capitalize())
            return list_db

    def connected(self):
        db = self.open_json()
        if db is not None:
            list_of_db = []
            for j in db:
                print(db.index(j) + 1, ' - ', j["name"])
                list_of_db.append(j)
            print()
            namedb = int(input("Enter with index of database: ")) - 1
            for k in list_of_db:
                if namedb == db.index(k):
                    self.host = k['uri']
                    self.database = k['databaseName']
                    self.user = k['user']
                    self.password = k['password']
                    self.__conn = ConnectDataBase(self.host, self.database, self.user, self.password)
                    if self.conn:
                        print(f"Conectado ao banco {k['name']}")
                    else:
                        print(f"Falha na conexão")
                    return self.conn
        else:
            return "Not found"

    def query_default(self, sql):
        result = self.conn.manipular(sql)
        if result:
            self.conn.close_connection()
            return f'Insert execultado:\n {sql}'
        else:
            self.conn.close_connection()
            return f'Falha ao executar o insert:\n {sql}'

    def query_user(self, sql):
        data = []
        result = self.conn.execute_query(sql)
        for row in result:
            data.append(row)
        json_data = json.dumps(data)
        convert_list = json.loads(json_data)
        self.conn.close_connection()
        return convert_list
