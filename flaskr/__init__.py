import os
from flask import Flask, app,render_template,redirect,request,session
import requests
from functools import wraps

login_data = [{'account': 'erp123', 'password': 'erp456'}]

def login_required(func):
	@wraps(func)#保留源信息，本質是endpoint裝飾，否則修改函數名很危險
	def inner(*args,**kwargs):#接收參數，*args接收多餘參數形成元組，**kwargs接收對於參數形成字典
		token=session.get('token') #表單接手網頁中登錄信息，存入到session中，判斷用戶是否登錄
		if not token:
			return redirect('/') #沒有登錄就跳轉到登錄路由下
		return func(*args,**kwargs)#登錄成功就執行傳過來的函數
	return inner


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['SECRET_KEY'] = b'123456789'
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
        return redirect('/loginpage')
    error_message = "Invalid account or password"
    
    @app.route('/loginpage', methods=['GET', 'POST'])
    def loginpage():
        if request.method == 'POST':
            account = request.form.get('account')
            password = request.form.get('password')
            for data in login_data:
                if data['account']==account and data['password']==password:
                    session['token'] = "yes"
                    return redirect("/myErp")    
        return render_template("loginpage.jinja", error_message=error_message)
    @app.route('/myErp')
    @login_required
    def myErp():
        return render_template('hello.jinja')
    @app.route('/myErp/staff')
    @login_required
    def staff():
        staffs = requests.get('http://127.0.0.1:5000/staff')
        return render_template('staff.jinja',staffs=staffs.json()['staff_list'])
    @app.route('/myErp/supplier')
    @login_required
    def supplier():
        suppliers = requests.get('http://127.0.0.1:5000/supplier')
        return render_template('supplier.jinja',suppliers=suppliers.json()['supplier_list'])
    @app.route('/myErp/member')
    @login_required
    def member():
        members = requests.get('http://127.0.0.1:5000/member')
        return render_template('member.jinja',members=members.json()['member_list'])
    @app.route('/myErp/item')
    @login_required
    def item():
        items = requests.get('http://127.0.0.1:5000/item')
        return render_template('item.jinja',items=items.json()['item_list'])
    @app.route('/myErp/purchase_order')
    @login_required
    def purchase_order():
        porders = requests.get('http://127.0.0.1:5000/purchase_order')
        return render_template('purchase_order.jinja',orders=porders.json()['p_order_list'])
    
    @app.route('/myErp/purchase_order/<pid>')
    @login_required
    def purchase_order_detail(pid):
        headers = {'Content-type': 'application/json'}
        porder_detail = requests.get('http://127.0.0.1:5000/purchase_order/detail',headers=headers,json={'p_order_id':pid})
        print(porder_detail)
        return render_template('purchase_order_detail.jinja',items=porder_detail.json()['item_list'])
    @app.route('/myErp/purchase_order/add')
    def purchase_order_add():
        staffs = requests.get('http://127.0.0.1:5000/staff').json()['staff_list']
        suppliers = requests.get('http://127.0.0.1:5000/supplier').json()['supplier_list']
        return render_template('purchase_order_add.jinja',suppliers=suppliers,staffs=staffs)
    @login_required
    @app.route('/myErp/sale_order')
    def sale_order():
        sorders = requests.get('http://127.0.0.1:5000/sale_order')
        return render_template('sale_order.jinja',orders=sorders.json()['s_order_list'])
    @app.route('/myErp/sale_order/<pid>')
    def sale_order_detail(pid):
        headers = {'Content-type': 'application/json'}
        sorder_detail = requests.get('http://127.0.0.1:5000/sale_order/detail',headers=headers,json={'s_order_id':pid})
        return render_template('sale_order_detail.jinja',items=sorder_detail.json()['item_list'])
    @app.route('/myErp/sale_order/add')
    def sale_order_add():
        items = requests.get('http://127.0.0.1:5000/item').json()['item_list']
        staffs = requests.get('http://127.0.0.1:5000/staff').json()['staff_list']
        members = requests.get('http://127.0.0.1:5000/member').json()['member_list']
        return render_template('sale_order_add.jinja',members=members,staffs=staffs,items=items)
    @app.route('/myErp/supplier_item')
    def revenue():
        suppliers = requests.get('http://127.0.0.1:5000/supplier')
        return render_template('supplier_item.jinja',suppliers=suppliers.json()['supplier_list'])

    from .api import (staff, supplier, member, item,purchase_order, sale_order,income,supplier_item)
    app.register_blueprint(staff.bp)
    app.register_blueprint(supplier.bp)
    app.register_blueprint(member.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(purchase_order.bp)
    app.register_blueprint(sale_order.bp)
    app.register_blueprint(income.bp)
    app.register_blueprint(supplier_item.bp)
    return app
  

