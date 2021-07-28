import datetime
import sqlite3


class Database:

    def __init__(self, path_to_db="data/Events.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False,
                fetchall=False, commit=False):
        # f"SELECT * FROM Users WHERE Id= {message.from_user.id}" """- неверная запись"""
        # "SELECT  * FROM Users(id, name, email) VALUES(?, ?, ?)"
        if not parameters:
            parameters = tuple()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def get_list_of_events(self):
        sql = f"""SELECT Id, Name FROM Event WHERE Date > {int(datetime.datetime.now().strftime("%m%d"))} OR 
        (Date = {int(datetime.datetime.now().strftime("%m%d"))} AND Time
         > {int(datetime.datetime.now().strftime("%H%M"))})"""
        return self.execute(sql, fetchall=True)

    def select_event(self, id: str):
        sql = f"SELECT Name, Date, Time, Place FROM Event WHERE Id = ?"
        data = id,
        return self.execute(sql, parameters=data, fetchall=True)

    def get_amount_of_places(self, id: str):
        sql = f"SELECT Capacity FROM Event WHERE Id = ? "
        data = id,
        return self.execute(sql, parameters=data, fetchone=True)

    def get_handled_places(self, id: str):
        sql = f"SELECT Quantity FROM Booking WHERE Event = ?"
        data = id,
        if sql:
            return self.execute(sql, parameters=data, fetchall=True)
        else:
            return "0"

    def book_the_event(self, id: str, user_id: str, amount: int):
        sql = f"INSERT INTO Booking(User, Event, Quantity) VALUES(?, ?, ?)"
        parameters = (user_id, id, amount)
        self.execute(sql, parameters=parameters, commit=True)

    def delete_users(self):
        sql = f"DELETE FROM Booking WHERE True"
        self.execute(sql, commit=True)

    def expired_events(self):
        sql = f"""SELECT Id FROM Event WHERE Date < {int(datetime.datetime.now().strftime("%m%d"))} OR 
                (Date = {int(datetime.datetime.now().strftime("%m%d"))} AND Time
                 < {int(datetime.datetime.now().strftime("%H%M"))})"""
        return self.execute(sql, fetchall=True)

    def my_orders(self, id: str):
        sql = f"""SELECT Event, Quantity  FROM Booking WHERE User = ?"""
        parameters = id,
        return self.execute(sql, parameters=parameters, fetchall=True)

    def description(self, id: str):
        sql = f"""SELECT Comment FROM Event WHERE Id = ?"""
        parameters = id,
        return self.execute(sql, parameters=parameters, fetchall=True)


def logger(statement):
    print(f"________________________________________________________ \n"
          f"Executing: \n"
          f"{statement} \n"
          f"_________________________________________________________"
          )
