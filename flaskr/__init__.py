import os
from flask import Flask, app,render_template,redirect,request
import requests
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
    
    # a simple page that says hello
    @app.route('/')
    def index():    
        return redirect('/loginpage')
    error_message = "Invalid account or password"
    login_data = [{'account': 'erp123', 'password': 'erp456'}]
    @app.route('/loginpage', methods=['GET', 'POST'])
    def loginpage():
        if request.method == 'POST':
            account = request.form.get('account')
            password = request.form.get('password')
            for data in login_data:
                if data['account']==account and data['password']==password:
                    return redirect("/myErp")    
        return render_template("loginpage.jinja", error_message=error_message)
    @app.route('/myErp')
    def myErp():
        return render_template('hello.jinja')
    @app.route('/myErp/staff')
    def staff():
        return render_template('staff.jinja',staffs=staffs)
    @app.route('/myErp/supplier')
    def supplier():
        suppliers = requests.get('http://127.0.0.1:5000/supplier')
        return render_template('supplier.jinja',suppliers=suppliers.json()['supplier_list'])
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
    
    @app.route('/myErp/purchase_order/add')
    def purchase_order_add():
        return render_template('purchase_order_add.jinja')
    
    @app.route('/myErp/sale_order')
    def sale_order():
        return render_template('sale_order.jinja',orders=porder)
    @app.route('/myErp/sale_order/<pid>')
    def sale_order_detail(pid):
        pid=int(pid)
        return render_template('sale_order_detail.jinja',items=[items[pid-1]])
    @app.route('/myErp/sale_order/add')
    def sale_order_add():
        return render_template('sale_order_add.jinja')
    
    @app.route('/add', methods=['GET', 'POST'])
    @app.route('/addsupplier', methods=['GET', 'POST'])
    def add():
        if request.method == 'POST':
            if request.path == '/add':
                staff_id = request.form.get('id')
                name = request.form.get('name')
                managerId = request.form.get('mId')
                staffs.append({'id': staff_id, 'name': name, 'mId': managerId})
                return redirect("/myErp/staff")
            elif request.path == '/addsupplier':
                supplier_id = request.form.get('id')
                Name = request.form.get('name')
                Phone = request.form.get('phone')
                Email = request.form.get('email')
                Address = request.form.get('address')
                suppliers.append({'id': supplier_id, 'name': Name, 'phone': Phone, 'email': Email, 'address': Address})
                return redirect("/myErp/supplier")
    
    @app.route('/delete', methods=['GET', 'POST'])
    @app.route('/deletesupplier', methods=['GET', 'POST'])
    def delete():
        if request.method == 'POST':
            id = request.form.get('id')
            if request.path == '/delete':
                for s in staffs:
                    if s['id'] == id:
                        staffs.remove(s)
                return redirect("/myErp/staff")
            elif request.path == '/deletesupplier':
                for s in suppliers:
                    if s['id'] == id:
                        suppliers.remove(s)
                return redirect("/myErp/supplier")
    @app.route('/modify', methods=['GET', 'POST'])
    @app.route('/modifysupplier', methods=['GET', 'POST'])
    def modify():
        if request.method == 'POST':
            id = request.form.get('id')
            if request.path == '/modify':
                name = request.form.get('name')
                managerId = request.form.get('mId')
                for s in staffs:
                    if s['id'] == id:
                        s['name'] = name
                        s['mId'] = managerId
                return redirect("/myErp/staff")
            elif request.path == '/modifysupplier':
                name = request.form.get('name')
                Phone = request.form.get('phone')
                Email = request.form.get('email')
                Address = request.form.get('address')
                for s in suppliers:
                    if s['id'] == id:
                        s['name'] = name
                        s['phone'] = Phone
                        s['email'] = Email
                        s['address'] = Address
                return redirect("/myErp/supplier")

    from .api import (staff, supplier, member, item,purchase_order, sale_order)
    app.register_blueprint(staff.bp)
    app.register_blueprint(supplier.bp)
    app.register_blueprint(member.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(purchase_order.bp)
    app.register_blueprint(sale_order.bp)
    return app
  

