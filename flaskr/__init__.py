import os
from flask import Flask, app,render_template,redirect,request

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
    suppliers = [{'id':'1','name':'ABC','email':'123456@gmail.com','phone':'0937957279','address':'台北市文山區指南路二段4號'}
                ,{'id':'2','name':'DEF','email':'78901@gmail.com','phone':'0938307320','address':'台北市文山區指南路一段78號'}]
    staffs = [{'id':'1','name':'Frank','mId':'2'},{'id':'2','name':'Rex','mId':''}]
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
        return render_template('supplier.jinja',suppliers=suppliers)
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
