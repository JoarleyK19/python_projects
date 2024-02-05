from dataBaseDAO.QueryDB import QueryDB


class InsertInvoiceClients(QueryDB):
    def __init__(self, last_month_date, current_month_date, date_month_end, first_day_of_current_month_date, host, db, usr, pwd):
        self.__last_month_date = last_month_date
        self.__current_month_date = current_month_date
        self.__date_month_end = date_month_end
        self.__first_day_of_current_month_date = first_day_of_current_month_date
        self.__list_id_client: list = []
        super(InsertInvoiceClients, self).__init__(host, db, usr, pwd)

    @property
    def last_month_date(self):
        return self.__last_month_date

    @last_month_date.setter
    def last_month_date(self, new_last_month_date):
        self.__last_month_date = new_last_month_date

    @property
    def current_month_date(self):
        return self.__current_month_date

    @current_month_date.setter
    def current_month_date(self, new_current_month_date):
        self.__current_month_date = new_current_month_date

    @property
    def date_month_end(self):
        return self.__date_month_end

    @date_month_end.setter
    def date_month_end(self, new_date_month_end):
        self.__date_month_end = new_date_month_end

    @property
    def list_id_client(self):
        return self.__list_id_client

    @list_id_client.setter
    def list_id_client(self, new_list_id_client):
        self.__list_id_client = new_list_id_client
        
    @property
    def first_day_of_current_month_date(self):
        return self.__first_day_of_current_month_date
    
    @first_day_of_current_month_date.setter
    def first_day_of_current_month_date(self, new_first_day_of_current_month_date):
        self.__first_day_of_current_month_date = new_first_day_of_current_month_date

    def get_actual_invoice(self):
        result = super().search_invoice(self.current_month_date)
        if result.error:
            return print(result.error)
        else:
            return result
    
    # def get_all_invoices_last_month(self):
    #     result = super().search_invoice_all(self.latest_date)
    #     if result.error:
    #         return print(result.error)
    #     else:
    #         return result

    def compare_invoices(self):
        result_compare = super().compare_invoices_for_month(self.last_month_date, self.current_month_date, self.date_month_end)
        if type(result_compare) is not list and result_compare.pgerror:
            print(result_compare)
            super().close_connection()
            return
        else:
            self.list_id_client = result_compare
            print(self.list_id_client)
            super().insert_invoice_date_now(self.list_id_client, self.first_day_of_current_month_date, self.current_month_date, self.last_month_date)
            super().close_connection()


        