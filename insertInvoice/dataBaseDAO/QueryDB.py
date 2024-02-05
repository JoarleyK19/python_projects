from dataBaseDAO.ConnectDataBase import ConnectDataBase
from model.helpUser import extract_int_of_list, extract_list_of_tupla, to_string


class QueryDB(ConnectDataBase):
    def __init__(self, host, db, usr, pwd):
        super(QueryDB, self).__init__(host, db, usr, pwd)
        self.__sql = None

    @property
    def sql(self):
        return self.__sql

    @sql.setter
    def sql(self, new_sql):
        self.__sql = new_sql

    def search_invoice(self, final_date):
        self.sql = f"""SELECT i.id_client FROM invoice i WHERE end_date = '{final_date}'"""
        result = self.search(self.sql)
        if result is None or len(result) == 0:
            return f"Not found invoice at date {final_date}"
        else:
            return result

    def search_invoice_all(self, latest_date):
        self.sql = f"""SELECT i.id_client FROM invoice i WHERE end_date = '{latest_date}'"""
        result = self.search(self.sql)
        if result is None or len(result) == 0:
            return f"Not found invoice at date {latest_date}"
        else:
            return result

    def compare_invoices_for_month(self, date_for_compare_last_month, date_for_compare_current_month, date_for_compare_end_month):
        self.sql = f"""select
                            i.id_client
                        from
                            invoice i
                        where
                            end_date = '{date_for_compare_last_month}'
                            and i.id_client not in (
                            select
                                i.id_client
                            from
                                invoice i
                            where
                                end_date >= '{date_for_compare_current_month}'
                                and end_date < '{date_for_compare_end_month}'
                            )"""
        print(self.sql)
        result = self.search(self.sql)
        return result

    def search_last_invoice(self, id_client: list, date_for_compare_end):
        newList = extract_list_of_tupla(id_client)
        print(newList)
        extractedList = extract_int_of_list(newList)
        print(extractedList)
        self.sql = f"""select
                            i.uuid
                        from
                            invoice i
                        where
                            i.id_client in ({extractedList})
                            and end_date = '{date_for_compare_end}'"""
        print(self.sql)
        result = self.search(self.sql)
        return result

    def insert_invoice_date_now(self, id_client: list, first_day_of_current_month_date, current_month_date, last_month_date):
        result_last_invoice = self.search_last_invoice(id_client, last_month_date)
        if type(result_last_invoice) is not list and result_last_invoice.pgerror:
            print(result_last_invoice)
            super().close_connection()
            return
        else:
            for i in result_last_invoice:
                self.sql = f""" INSERT INTO invoice (id_account, reference, start_date, end_date, created, processed_key, total,
                                                        total_classes_json, headerinfotojson, id_client, id_affiliate, json_info, uuid)
                                        select id_account, reference, '{first_day_of_current_month_date}',
                                            '{current_month_date}', created, '{current_month_date}',
                                            total, total_classes_json, headerinfotojson, id_client, id_affiliate, json_info, uuid_generate_v4()
                                        FROM invoice i
                                        WHERE i.uuid = {to_string(i)}; """
                try:
                    result = self.manipulate(self.sql)
                    return f'Insert realized success!!! {result}'
                except Exception as e:
                    super().close_connection()
                    return print(e)
        super().close_connection()
