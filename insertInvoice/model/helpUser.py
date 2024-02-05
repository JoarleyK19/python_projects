from datetime import datetime, timedelta

from service.SelectDataBase import OpenDataBase


def sql_user():
    print('Digite sua query:')
    sql = input()
    return sql


def format_date_month_init(date_month_init):
    date_formatted = date_month_init.strftime("%Y-%m-%d")
    return date_formatted


def format_date_month_end(date_month_end):
    date_formatted = date_month_end.strftime("%Y-%m-%d")
    return date_formatted


def to_string(list_service: list):
    new_string = ''
    for i in list_service:
        string = f"'{i}',"
        new_string += string
    return new_string[:-1]


def to_int(list_string):
    new_int = list(map(int, list_string))
    return new_int


def to_list(lists):
    new_list = lists.split(',')
    return new_list


def extract_list_of_tupla(lista):
    new_list = []
    for i in lista:
        for j in i:
            new_list.append(j)
    return new_list


def extract_int_of_list(list_int):
    values = ", ".join(str(valor) for valor in list_int)
    return values


def tested():
    t = OpenDataBase('databases.json')
    t.query_user('SELECT * FROM test')
    list_teste = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    extract_int_of_list(list_teste)


