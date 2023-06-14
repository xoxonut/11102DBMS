import os
from flask import url_for
from flask import Flask, render_template, redirect, request
from flask import Flask, request, jsonify


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
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
    @app.route("/")
    def index():
        return redirect("/myErp")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            staff_id = request.form.get("staff_id")
            password = request.form.get("password")
            return redirect("/myErp")
        return render_template("login.jinja")

    @app.route("/myErp")
    def myErp():
        return render_template("hello.jinja")

    @app.route("/myErp/staff")
    def staff():
        return redirect(url_for("staff"))

    @app.route("/myErp/supplier")
    def supplier():
        return redirect(url_for("supplier"))

    @app.route("/myErp/member")
    def member():
        return redirect(url_for("member"))

    @app.route("/myErp/item", methods=["GET", "PUT"])
    def item():
        return "123"
        # return redirect(url_for("item"))
        # return jsonify(read_item())

    @app.route("/myErp/purchase_order")
    def purchase_order():
        return redirect(url_for("purchase_order"))

    @app.route("/myErp/sale_order")
    def sale_order():
        return redirect(url_for("sale_order"))

    @app.route("/myErp/income")
    def income():
        return redirect(url_for("income"))

    @app.route("/myErp/staff_performance")
    def staff_performance():
        return redirect(url_for("staff_performance"))

    @app.route("/add", methods=["GET", "POST"])
    def add():
        if request.method == "POST":
            staff_id = request.form.get("id")
            name = request.form.get("name")
            managerId = request.form.get("mId")
            staffs.append({"id": staff_id, "name": name, "mId": managerId})
            return redirect("/myErp/staff")
        return render_template("add.jinja")

    from .api import staff, supplier, member, item, purchase_order, sale_order, income, staff_performance

    app.register_blueprint(staff.bp)
    app.register_blueprint(supplier.bp)
    app.register_blueprint(member.bp)
    app.register_blueprint(item.bp)
    app.register_blueprint(purchase_order.bp)
    app.register_blueprint(sale_order.bp)
    app.register_blueprint(income.bp)
    app.register_blueprint(staff_performance.bp)
    return app
