import sqlite3
import threading

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class MetaSingleConnection(type):

    _instance = dict()
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instance:
                inst = super().__call__(*args, **kwargs)
                cls._instance[cls] = inst

            return cls._instance[cls]

class SingleConnection(metaclass = MetaSingleConnection):
    db = None
    def __init__(self):
        pass

    def get_cursor(self):
        return self.db.cursor()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
        del self

class SQLiteConnection(SingleConnection):
    def __init__(self):
        path = "test.sqlite"
        self.db = sqlite3.connect(path)
        self.db.row_factory = dict_factory

class DataSet():
    main_table = None
    columns = dict()
    pk = False
    result_obj = lambda *args, **kwargs: args
    def __init__(self):
        self.cursor = SQLiteConnection().get_cursor()
        self.make_main_requests()
    
    def make_main_requests(self):
        self.select = "SELECT {columns} FROM {table}".format(
            columns = ", ".join([column for column in self.columns]),
            table = self.main_table,
        )

    def get_all(self):
        self.cursor.execute(
            self.select + ";"
        )
        result = list()
        item = self.cursor.fetchone()
        while item:
            result.append(self.result_obj(item, parent = self.__class__, cursor = self.cursor))
            item = self.cursor.fetchone()
        return result

    def get(self, **kwargs):
        request = "SELECT {columns} FROM {table} WHERE {conditions};".format(
            columns = ", ".join(column for column in self.columns),
            table = self.main_table,
            conditions = ", ".join([column + " = %s" for column in kwargs if column in self.columns])
        )
        self.cursor.execute(request % tuple("\'" + str(kwargs[column]) + "\'" for column in kwargs if column in self.columns))
        # print(request % tuple("\'" + str(kwargs[column]) + "\'" for column in kwargs if column in self.columns))
        # self.cursor.execute(
        #     request % tuple("\'" + str(kwargs[column]) + "\'" for column in kwargs if column in self.columns)
        # )
        result = list()
        item = self.cursor.fetchone()
        while item:
            result.append(self.result_obj(item, parent = self.__class__, cursor = self.cursor))
            item = self.cursor.fetchone()
        return result

class ResultItem():
    _parent = None
    _dict = dict()
    def __init__(self, data, parent = None, cursor = None):
        self._parent = parent
        self._curs = cursor
        for column in data:
            self._dict[column] = data[column]

    def set_value(self, **kwargs):
        request = "UPDATE {table} SET {values} WHERE id={id};".format(
            table = self._parent.main_table,
            values = ", ".join(item + "=%s" for item in kwargs if item in self._parent.columns),
            id = self._dict["id"]
        )
        SQLiteConnection().get_cursor().execute(request % tuple(kwargs[item] for item in kwargs if item in self._parent.columns))
        SQLiteConnection().commit()
        # print(request % tuple(kwargs[item] for item in kwargs if item in self._parent.columns))
        
class Session(DataSet):
    main_table = "session"
    columns = {
        "id": {"type": 1, "null": False, "unique": True, },                 # Первичный ключ
        "hash_key": {"type": 2, "null": False, "unique": True, },           # Ключ для сессии
        "create_date": {"type": 1, "null": False, "unique": False, },       # Дата создания сессии
        "renew_date": {"type": 1, "null": False, "unique": False, },        # Дата последнего обновления ключа сессии
        "removed": {"type": 1, "null": True, "unique": False, },            # Пометка об удалении      
    }
    pk = {"column": "id", "ai": True}
    result_obj = ResultItem

if __name__ == "__main__":

    pass
    