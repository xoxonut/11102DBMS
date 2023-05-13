import os

from flask import Flask,render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('hello.jinja')
    @app.route('/t')
    def t():
        return '123'
    from .api import (staff, supplier, member, item,purchase_order, sale_order)
    app.register_blueprint(staff.bp)
    app.register_blueprint(supplier.bp)
    app.register_blueprint(member.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(purchase_order.bp)
    app.register_blueprint(sale_order.bp)
    return app
