import os

from flask import Flask,render_template,redirect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    from . import db
    db.init_app(app)
    
    # a simple page that says hello
    @app.route('/')
    def index():    
        return redirect('/myErp')
    @app.route('/myErp')
    def myErp():
        return render_template('hello.jinja')
    @app.route('/myErp/staff')
    def staff():
        return '123'
    @app.route('/myErp/supplier')
    def supplier():
        return '123'
    @app.route('/myErp/member')
    def member():
        return '123'
    @app.route('/myErp/item')
    def item():
        return '123'
    @app.route('/myErp/purchase_order')
    def purchase_order():
        return '123'
    @app.route('/myErp/sale_order')
    def sale_order():
        return '123'
    from .api import (staff, supplier, member, item,purchase_order, sale_order)
    app.register_blueprint(staff.bp)
    app.register_blueprint(supplier.bp)
    app.register_blueprint(member.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(purchase_order.bp)
    app.register_blueprint(sale_order.bp)
    return app
