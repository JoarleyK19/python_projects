# This is a sample Python script.
from service.InsertInvoiceClients import InsertInvoiceClients
from service.SelectDataBase import OpenDataBase


# Press Alt+Shift+X to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def init_app():
    name_json = input("Enter with name json: ")
    connected_db = OpenDataBase(name_json)
    connected_db.connected()
    initial_date = input("Enter last month date: (YYYY-MM-DD) ")
    final_date = input("Enter current month date: (YYYY-MM-DD) ")
    date_month_end = input("Enter month end date: (YYYY-MM-DD) ")
    first_day_of_current_month_date = input("Enter first day of current month date: (YYYY-MM-DD) ")

    insert_invoice_clients = InsertInvoiceClients(initial_date, final_date, date_month_end, first_day_of_current_month_date, connected_db.host,
                                                  connected_db.database, connected_db.user, connected_db.password)

    print(insert_invoice_clients.compare_invoices())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init_app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
