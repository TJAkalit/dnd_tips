from sqlite3 import connect
from flask import Flask
from flask import Request
from flask import redirect
from flask import render_template
from flask import make_response
import logging
import hashlib
import datetime

if __name__ == "__main__":

    app = Flask(__name__)
    
    @app.route("/")
    @app.route("/index.html")
    @app.route("/index.php")
    def index():
        
        return render_template(
            "index.html",
            title = "dnd_tips index page"
        )       

    app.run()