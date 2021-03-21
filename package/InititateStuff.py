import sqlite3
import logging
import DataBase

class Initiator():

    TYPES = {1: "INTEGER", 2: "TEXT", 3: "REAL",}

    def __init__(self, cls):
        self.cls = cls
        self.connection = sqlite3.connect("test.sqlite")
        self.cursor = self.connection.cursor()
    
    def table_maker(self):
        request = "CREATE TABLE IF NOT EXISTS {table_name} \n(".format(
            table_name = self.cls.main_table
        )
        for column in self.cls.columns:
            request += " {name} {data_type}{isnull}{unique},\n".format(
                name = column,
                data_type = self.TYPES[self.cls.columns[column]["type"]],
                isnull = " NOT NULL" if not self.cls.columns[column]["null"] else "",
                unique = " UNIQUE" if self.cls.columns[column]["unique"] else "",
            )
        if self.cls.pk:
            request += "PRIMARY KEY (\"{pk}\"{ai})".format(
                pk = self.cls.pk["column"],
                ai = " AUTOINCREMENT" if self.cls.pk["ai"] else ""
            )

        request += "\n);"
        self.cursor.execute(
            request
        )
        self.connection.commit()
        self.connection.close()

if __name__ == "__main__":
    for table in [DataBase.Session]:
        Initiator(table).table_maker()