import sqlite3
import pandas as pd
from sqlite3 import Error

class DBConn:

    def __init__(self) -> None:

        self.conn = None


    def connect(self) -> None:

        try:
            self.conn = sqlite3.connect("local_database.db")
        except Error as err:
            raise(f"sqlite connection error: {err}")


    def disconnect(self)-> None:

        if self.conn is not None:
            self.conn.close()


    def create_table(self) -> None:

        try:
            with self.conn:
                self.conn.execute("CREATE TABLE IF NOT EXISTS monthlydates(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, axis INTEGER, shares INTEGER, pension INTEGER, lisa INTEGER, total INTEGER)")
                self.conn.commit()
        except Error as err:
            raise(f"sqlite connection error: {err}")


    def read_db(self) -> pd.DataFrame:

        try:
            df = pd.read_sql_query("SELECT * FROM monthlydates", self.conn)
            df.sort_values(by='date', ascending=True, inplace=True)
            return df.to_dict(orient="records")
        except Error as err:
            raise(f"sqlite connection error: {err}")


    def add_record(self, date: str, axis:int, shares:int, pension:int, lisa:int, total:int) -> None:

        try:
            with self.conn:
                row_id = self.conn.execute("SELECT MAX(id) + 1 FROM monthlydates").fetchone()[0]
                data = (row_id, date, axis, shares, pension, lisa, total)
                self.conn.execute("INSERT INTO monthlydates values (?, ?, ?, ?, ?, ?, ?)", data)
                self.conn.commit()
        except Error as err:
            raise(f"sqlite connection error: {err}")


    def edit_record(self, row_id: int, axis:int, shares:int, pension:int, lisa:int) -> None:

        print(axis, shares, pension, lisa)

        total = axis + shares + pension + lisa

        try:
            with self.conn:
                # data = (row_id, date, axis, shares, pension, lisa, total)
                self.conn.execute("UPDATE monthlydates SET axis = ?, shares = ?, pension = ?, lisa = ?, total = ? WHERE id = ?",
                                  (axis, shares, pension, lisa, total, row_id))
                self.conn.commit()
        except Error as err:
            raise(f"sqlite connection error: {err}")


    def del_record(self, row_id: int) -> None:

        try:
            with self.conn:
                self.conn.execute("DELETE FROM monthlydates WHERE id = ?", (row_id,))
                self.conn.commit()
        except Error as err:
            raise(f"sqlite connection error: {err}")


    def create_df(self) -> pd.DataFrame:

        df = pd.read_sql_query("SELECT * FROM monthlydate", self.conn)
        df = df.rename({
            'id': 'id',
            'date': 'Date',
            'axis': 'Axis',
            'shares': 'Shares',
            'pension': 'Pension',
            'lisa': 'LISA',
            'total': 'Total'})
        # Coverting string to datetime and integers
        for col in ['id', 'Axis', 'Shares', 'Pension', 'LISA', 'Total']:
            df[col] = df[col].astype('int64')
        df = df.sort_values(by='Date', ascending=True)
        return df