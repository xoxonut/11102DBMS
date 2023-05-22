import os

from flask import Flask,render_template,redirect,request


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
    staffs = [{'id':'1','name':'Frank','mId':'2'},{'id':'2','name':'Rex','mId':''}]
    members =[{'id':'1','name':'Frank','email':'frank@gmail.com','phone':'0966513967','address':'235新北市中和區中正路291號'},
            {'id':'2','name':'Rex','email':'sad@gmail.com','phone':'0966513967','address':'235新北市中和區中正路291號'}]
    items = [{'id':1,'name':'apple','type':'fruit','unit_price':100,'stock':1984},
            {'id':2,'name':'banana','type':'fruit','unit_price':50,'stock':1984}]
    porder = [{'id':1,'supplier_id':1,'staff_id':1},
            {'id':2,'supplier_id':2,'staff_id':2}]
    # a simple page that says hello
    @app.route('/')
    def index():    
        return redirect('/myErp')
    @app.route('/login',methods=['GET','POST'])
    def login():    
        if request.method=='POST':
            staff_id=request.form.get('staff_id')
            password=request.form.get('password')
            return redirect("/myErp")
        return render_template("login.jinja")
    
    
    @app.route('/myErp')
    def myErp():
        return render_template('hello.jinja')
    
    
    @app.route('/myErp/staff')
    def staff():
        return render_template('staff.jinja',staffs=staffs)
    
    
    @app.route('/myErp/supplier')
    def supplier():
        return '123'
    
    
    @app.route('/myErp/member')
    def member():
        return render_template('member.jinja',members=members)
    
    
    @app.route('/myErp/item')
    def item():
        return render_template('item.jinja',items=items)
    
    
    @app.route('/myErp/purchase_order')
    def purchase_order():
        return render_template('purchase_order.jinja',orders=porder)
    
    @app.route('/myErp/purchase_order/<pid>')
    def purchase_order_detail(pid):
        pid=int(pid)
        return render_template('purchase_order_detail.jinja',items=[items[pid-1]])
    
    @app.route('/myErp/sale_order')
    def sale_order():
        return '123'
    
    
    @app.route('/add',methods=['GET','POST'])
    def add():
        if request.method=='POST':
            staff_id=request.form.get('id')
            name=request.form.get('name')
            managerId=request.form.get('mId')
            staffs.append({'id': staff_id, 'name': name, 'mId': managerId})
            return redirect("/myErp/staff")  
        return render_template('add.jinja')
    
    from .api import (staff, supplier, member, item,purchase_order, sale_order)
    app.register_blueprint(staff.bp)
    app.register_blueprint(supplier.bp)
    app.register_blueprint(member.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(purchase_order.bp)
    app.register_blueprint(sale_order.bp)
    return app
