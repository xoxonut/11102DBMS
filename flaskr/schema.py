import sqlite3

conn = sqlite3.connect("instance/flaskr.sqlite")
cursor = conn.cursor()

staff = """CREATE TABLE STAFF(
            staff_id INT PRIMARY KEY NOT NULL,
            manager_id INT,
            name CHAR(20) NOT NULL, 
            entry_date DATE,
            FOREIGN KEY(manager_id) REFERENCES STAFF(staff_id)
            )"""
cursor.execute(staff)

supplier = """CREATE TABLE SUPPLIER(
                supplier_id INT PRIMARY KEY,
                name CHAR(20) NOT NULL,
                email CHAR(30),
                phone_number CHAR(10),
                address CHAR(50)
                )"""
cursor.execute(supplier)

member = """CREATE TABLE MEMBER(
                member_id INT PRIMARY KEY,
                name CHAR(20) NOT NULL,
                email CHAR(30),
                phone_number CHAR(10),
                address CHAR(50)
                )"""
cursor.execute(member)

item = """CREATE TABLE ITEM(
            item_id INT PRIMARY KEY,
            name CHAR(20) NOT NULL,
            type CHAR(30),
            stock INT,
            unit_price INT
            )"""
cursor.execute(item)

purchase_order = """CREATE TABLE PURCHASE_ORDER (
                        p_order_id INT PRIMARY KEY,
                        supplier_id INT,
                        staff_id INT,
                        p_order_date DATE,
                        FOREIGN KEY (supplier_id) REFERENCES SUPPLIER(supplier_id),
                        FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id)
                        )"""
cursor.execute(purchase_order)

sales_order = """CREATE TABLE SALES_ORDER (
                    s_order_id INT PRIMARY KEY,
                    staff_id INT,
                    member_id INT,
                    s_order_date DATE,
                    FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id),
                    FOREIGN KEY (member_id) REFERENCES MEMBER(member_id)
                    )"""
cursor.execute(sales_order)

increase = """CREATE TABLE INCREASE (
                item_id INT PRIMARY KEY,
                p_order_id INT,
                unit_cost INT,
                item_quantity INT,
                FOREIGN KEY (p_order_id) REFERENCES PURCHASE_ORDER(p_order_id)
                )"""
cursor.execute(increase)

decrease = """CREATE TABLE DECREASE (
                item_id INT PRIMARY KEY,
                s_order_id INT,
                item_quantity INT,
                FOREIGN KEY (s_order_id) REFERENCES SALES_ORDER(s_order_id)
                )"""
cursor.execute(decrease)

conn.commit()
conn.close()
