import sqlite3

conn = sqlite3.connect("instance/flaskr.sqlite")
cursor = conn.cursor()

staff = """CREATE TABLE STAFF(
            staff_id INTEGER PRIMARY KEY,
            manager_id INTEGER,
            name CHAR(20) NOT NULL, 
            entry_date TEXT,
            FOREIGN KEY(manager_id) REFERENCES STAFF(staff_id)
            )"""
cursor.execute(staff)

supplier = """CREATE TABLE SUPPLIER(
                supplier_id INTEGER PRIMARY KEY,
                name CHAR(20) NOT NULL,
                email CHAR(30),
                phone_number CHAR(10),
                address CHAR(50)
                )"""
cursor.execute(supplier)

member = """CREATE TABLE MEMBER(
                member_id INTEGER PRIMARY KEY,
                name CHAR(20) NOT NULL,
                email CHAR(30),
                phone_number CHAR(10),
                address CHAR(50)
                )"""
cursor.execute(member)

item = """CREATE TABLE ITEM(
            item_id INTEGER PRIMARY KEY,
            name CHAR(20) NOT NULL,
            type CHAR(30),
            stock INTEGER,
            unit_price INTEGER
            )"""
cursor.execute(item)

purchase_order = """CREATE TABLE PURCHASE_ORDER (
                        p_order_id INTEGER PRIMARY KEY,
                        supplier_id INTEGER,
                        staff_id INTEGER,
                        p_order_date TEXT,
                        FOREIGN KEY (supplier_id) REFERENCES SUPPLIER(supplier_id),
                        FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id)
                        )"""
cursor.execute(purchase_order)

sales_order = """CREATE TABLE SALES_ORDER (
                    s_order_id INTEGER PRIMARY KEY,
                    staff_id INTEGER,
                    member_id INTEGER,
                    s_order_date TEXT,
                    FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id),
                    FOREIGN KEY (member_id) REFERENCES MEMBER(member_id)
                    )"""
cursor.execute(sales_order)

increase = """CREATE TABLE INCREASE (
                item_id INTEGER,
                p_order_id INTEGER,
                unit_cost INTEGER,
                item_quantity INTEGER,
                PRIMARY KEY (item_id, p_order_id),
                FOREIGN KEY (item_id) REFERENCES ITEM(item_id)
                FOREIGN KEY (p_order_id) REFERENCES PURCHASE_ORDER(p_order_id)
                )"""
cursor.execute(increase)

decrease = """CREATE TABLE DECREASE (
                item_id INTEGER,
                s_order_id INTEGER,
                item_quantity INTEGER,
                PRIMARY KEY (item_id, s_order_id),
                FOREIGN KEY (item_id) REFERENCES ITEM(item_id)
                FOREIGN KEY (s_order_id) REFERENCES SALES_ORDER(s_order_id)
                )"""
cursor.execute(decrease)

conn.commit()
conn.close()
