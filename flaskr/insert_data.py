import sqlite3

conn = sqlite3.connect("instance/flaskr.sqlite")
cursor = conn.cursor()

decrease_data = [
    (1, 10, 5),
    (2, 50, 3),
    (3, 80, 40),
]

insert_query = (
    "INSERT INTO decrease (item_id, s_order_id, item_quantity) VALUES (?, ?, ?)"
)

cursor.executemany(insert_query, decrease_data)

conn.commit()

conn.close()
