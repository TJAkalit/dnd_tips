from sqlite3 import connect
from flask import Flask
from flask import Request
from flask import redirect
from flask import render_template
import logging
import hashlib
import datetime

from background_static.templates import tables_template

def init_tables(db_file):

    try:
    
        db_file = str(db_file)
        db = connect(db_file)
    
    except Exception as ex:
        
        logging.error(
            "[INIT_TABLES] DB connect failed! {Except:s}".format(
                Except = ex
            )
        )

    curs = db.cursor()

    # Tables name check
    curs.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'""")
    temp = curs.fetchall()
    todo_tables = set(x for x in tables_template)

    for i in temp:
        
        todo_tables.discard(i[0])

    for table in todo_tables:

        logging.warning(
                "[INIT_TABLES] not found table [{not_found_table}]".format(
                    not_found_table = table
                )
            )

    for table in todo_tables:

        generated_query = ""
        generated_query += """CREATE TABLE IF NOT EXISTS {table_name} \n(""".format(table_name = table)
        d = dict()
                
        for column in tables_template[table]:

            if column in {"p_k", "f_k"}: continue

            d["name"] = column
            d["data_type"] = {
                1: "INTEGER",
                2: "TEXT",
                3: "REAL",
                4: "BLOB",
            }[tables_template[table][column]["type"]]
            d["isnull"] = " NOT NULL" if not tables_template[table][column]["null"] else ""
            d["unique"] = " UNIQUE" if tables_template[table][column]["unique"] else ""

            generated_query += """ {name} {data_type}{isnull}{unique},\n""".format(
                name = column,
                data_type = d["data_type"],
                isnull = d["isnull"],
                unique = d["unique"],
            )
        if tables_template[table]["p_k"]["exist"]:

            generated_query += """PRIMARY KEY (\"{column}\"{ai})""".format(
                column = tables_template[table]["p_k"]["column"],
                ai = " AUTOINCREMENT" if tables_template[table]["p_k"]["autoincrement"] else ""
            )

        if tables_template[table]["f_k"]["exist"]:
            pass
            # TODO: обработка инстркции вторичного ключа
            
        generated_query += "\n);"
        print(generated_query)
        ########
        # TODO: прописать параметры таблиц
        # TODO: выполнение предгенерированных запросов
        ########

class SessionManager:

    def __init__(self):

        try:
            self.db = connect("sessions.sqlite")
        except Exception:
            logging.error("Error at connect to DB")

        self.init_tables()

    def init_tables(self, table_template = None):

        cursor = self.db.cursor()

        d = {
            "session": """
            CREATE TABLE IF NOT EXISTS
            session (
                id INTEGER NOT NULL UNIQUE,
                hash_key TEXT NOT NULL UNIQUE,
                realm_id INTEGER,
                character_id INTEGER,
                removed INTEGER,
                create_date INTEGER NOT NULL,
                last_request INTEGER NOT NULL,
                PRIMARY KEY ("id" AUTOINCREMENT)
            );
            """
        }

        if table_template:

            cursor.execute(
                d[table_template]
            )
        else:

            for i0 in d:
                cursor.execute(d[i0])

        self.db.commit()

    def make_new(self) -> str:

        cursor = self.db.cursor()
        d_t = datetime.datetime.now()
        hash_key = hashlib.sha256(str(d_t).encode("utf-8")).hexdigest()
        create_date = int(d_t.timestamp())
        cursor.execute(
            f"""
            INSERT INTO session (hash_key, create_date, last_request) VALUES ("{hash_key}", "{create_date}", "{create_date}");
            """
        )
        self.db.commit()

        return hash_key
    
    def close_session(self, hash_key: str) -> bool:

        try:
            cursor = self.db.cursor()
            cursor.execute(
                f"""
                DELETE FROM session WHERE hash_key = "{hash_key}";
                """
            )
            self.db.commit()
        except Exception:

            logging.error("Fail on closing session!")

    def renew_key(self, hash_key_old: str) -> str:

        try:
            cursor = self.db.cursor()
            cursor.execute(
                f"""
                SELECT id FROM session WHERE hash_key = "{hash_key_old}";
                """
            )
            temp = cursor.fetchall()
            if temp.__len__() != 0:
                d_t = datetime.datetime.now()
                hash_key = hashlib.sha256(str(d_t).encode("utf-8")).hexdigest()
                create_date = int(d_t.timestamp())
                
                
                cursor.execute(
                    f"""UPDATE session SET hash_key = "{hash_key}", last_request = "{create_date}" WHERE hash_key = "{hash_key_old}";"""
                )
                self.db.commit()

        except Exception as ex:
            logging.error(f"Fail on renew hash key! {ex}")
        
        else:
            return hash_key

if __name__ == "__main__":

    app = Flask(__name__)
    SM = SessionManager()

    init_tables("sessions.sqlite")
    @app.route("/")
    @app.route("/index.html")
    @app.route("/index.php")
    def index():
        
        return render_template(
            "index.html",
            title = "dnd_tips index page"
        )       

    app.run()