from sqlite3 import connect
from flask import Flask
from flask import Request
from flask import redirect
from flask import render_template
import logging
import hashlib
import datetime

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

    @app.route("/")
    @app.route("/index.html")
    @app.route("/index.php")
    def index():
        
        return render_template(
            "index.html",
            title = "dnd_tips index page"
        )       

    app.run()