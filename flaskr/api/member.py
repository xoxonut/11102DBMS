from flask import Blueprint,render_template
from flaskr.db import get_db
from random import randint
bp = Blueprint('member', __name__, url_prefix='/member')

@bp.route('/')
def index():
    db = get_db()
    # db.execute(
    #                 "INSERT INTO user (username, password) VALUES (?, ?)",
    #                 (str(randint(1,234)), '123456'),
    # )
    # db.commit()
    user = db.execute("SELECT * FROM user").fetchone()
    return render_template('hello.jinja',user=user[1])