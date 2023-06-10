import sqlite3

conn = sqlite3.connect("instance/flaskr.sqlite")
cursor = conn.cursor()

# supplier_data = [
#     ("apple", "apple@apple.com", "1234567890", "Cupertino, California, United States"),
#     ("tesla", "tesla@tesla.com", "9876543210", "Austin, Texas, United States"),
#     (
#         "tsmc",
#         "tsmc@tsmc.com",
#         "1357924680",
#         "8, Li-Hsin Rd. 6, Hsinchu Science Park,Hsinchu 300-096, Taiwan, R.O.C.",
#     ),
# ]

# insert_query = (
#     "INSERT INTO supplier (name, email, phone_number, address) VALUES (?, ?, ?, ?)"
# )

# cursor.executemany(insert_query, supplier_data)
# conn.commit()

# member_data = [
#     ("Tom", "tom@gmail.com", "1122334455", "singapore"),
#     ("Emma", "emma@gmail.com", "6677889900", "usa"),
#     (
#         "Jack",
#         "jack@gmail.com",
#         "5544332211",
#         "thailand",
#     ),
# ]

# insert_query = (
#     "INSERT INTO member (name, email, phone_number, address) VALUES (?, ?, ?, ?)"
# )

# cursor.executemany(insert_query, member_data)
# conn.commit()

# item_data = [
#     ("iphone 14", "mobile phone", 10, 100),
#     ("model x", "car", 5, 1000),
#     ("M2", "chip", 50, 100),
# ]

# insert_query = "INSERT INTO item (name, type, stock, unit_price) VALUES (?, ?, ?, ?)"

# cursor.executemany(insert_query, item_data)
# conn.commit()

# cursor.execute('delete from staff where manager_id=""')
# staff_data = [
#     ("NULL", "John", "2023-5-20"),
#     (1, "Michael", "2023-5-21"),
#     (1, "Steve", "2023-5-21"),
# ]

# insert_query = "INSERT INTO staff (manager_id, name, entry_date) VALUES (?, ?, ?)"

# cursor.executemany(insert_query, staff_data)
# conn.commit()

# purchase_data = [
#     (1, 2, "2023-5-22"),
#     (2, 3, "2023-5-22"),
#     (3, 1, "2023-5-23"),
# ]

# insert_query = (
#     "INSERT INTO purchase_order (supplier_id, staff_id, p_order_date) VALUES (?, ?, ?)"
# )

# cursor.executemany(insert_query, purchase_data)
# conn.commit()

# sales_data = [
#     (2, 1, "2023-5-24"),
#     (2, 3, "2023-5-24"),
#     (3, 1, "2023-5-25"),
# ]

# insert_query = (
#     "INSERT INTO sales_order (staff_id, member_id, s_order_date) VALUES (?, ?, ?)"
# )

# cursor.executemany(insert_query, sales_data)
# conn.commit()

# increase_data = [
#     (1, 1, 10, 10),
#     (2, 2, 50, 5),
#     (3, 3, 80, 50),
# ]

# insert_query = "INSERT INTO increase (item_id, p_order_id, unit_cost, item_quantity) VALUES (?, ?, ?, ?)"

# cursor.executemany(insert_query, increase_data)
# conn.commit()

# decrease_data = [
#     (1, 10, 5),
#     (2, 50, 3),
#     (3, 80, 40),
# ]

# insert_query = (
#     "INSERT INTO decrease (item_id, s_order_id, item_quantity) VALUES (?, ?, ?)"
# )

# cursor.executemany(insert_query, decrease_data)
# conn.commit()

conn.close()
