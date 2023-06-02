from flask import Blueprint, jsonify, request
from flaskr.db import get_db
import datetime
import random

bp = Blueprint('sale_order', __name__, url_prefix='/sale_order')

@bp.route('/', methods=['DELETE'])
def delete_sales_order():
    return 'Sale Order index page'

@bp.route('/', methods=['GET'])
def read_sales_order():
  db = get_db()
  cursor = db.execute("""
      SELECT s_order_id, M.name AS member_name, ST.name AS staff_name, s_order_date
      FROM SALES_ORDER S, MEMBER M, STAFF ST
      WHERE S.member_id = M.rowid AND S.staff_id = ST.rowid""")
  rows = cursor.fetchall()

  order_list=[]
  for row in rows:
    s_order_id, member_name,  staff_name, s_order_date = row
    order = {
      "s_order_id": s_order_id,
      "member_name": member_name,
      "staff_name": staff_name,
      "s_order_date": s_order_date
    }
    order_list.append(order)

  db.close()
  
  
  return jsonify({"s_order_list": order_list})
  
@bp.route('/', methods=['POST'])
def create_sale_order():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    member_id = request.json.get('member_id')
    staff_id = request.json.get('staff_id')
    item_list = request.json.get('item_list')

    # check if staff exist
    db = get_db()
    cursor = db.execute("SELECT COUNT(*) AS result FROM STAFF WHERE rowid=?", [staff_id])
    rows = cursor.fetchall()
    if (rows[0]['result'] != 1):
      return {"error": "The staff doesn't exist!"}
    
    # check if member exist
    cursor = db.execute("SELECT COUNT(*) AS result FROM MEMBER WHERE rowid=?", [member_id])
    rows = cursor.fetchall()
    if (rows[0]['result'] != 1):
      return {"error": "This member doesn't exist!"}
    
    # insert into sale order
    s_order_date = datetime.datetime.now().strftime("%c")
    s_order_id = random.randint(1000, 100000) # this line should delete after DB modified to rowid
    cursor = db.execute("""INSERT INTO SALES_ORDER(s_order_id, staff_id, member_id, s_order_date) 
      VALUES (?,?,?,?)""", [s_order_id, staff_id, member_id, s_order_date]) 

    cursor = db.execute("SELECT rowid FROM SALES_ORDER WHERE staff_id = ? AND member_id = ? AND s_order_date=?", [staff_id, member_id, s_order_date])
    rows = cursor.fetchall()
    s_order_id = rows[0][0]
    print("create order: "+str(s_order_id))
    
    # check item 
    for item in item_list:
      item_name = item.get('name')
      item_type = item.get('type')
      item_quantity = item.get('quantity')

      # check if the item exist. 
      cursor = db.execute("SELECT COUNT(*) AS result FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      if (rows[0]['result'] != 1):
        #item doesn't exist
        return {"error": "The item doesn't exist!"}
      
      # check if item has unit price
      cursor = db.execute("SELECT unit_price AS result FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      if (rows[0]['result']== "Null"):
        return {"error": "The item doesn't have unit price!"}
    
      # check if item stock is enough
      cursor = db.execute("SELECT stock AS result FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      initial_item_stock = int(rows[0]['result'])
      if(initial_item_stock<int(item_quantity)):
        return {"error": "The item stock is not enough!"}

      # update item stock      
      print("initial stock: "+str(initial_item_stock))
      new_item_stock = initial_item_stock - item_quantity
      cursor = db.execute("UPDATE ITEM SET stock = ? WHERE name = ? AND type = ?", [new_item_stock, item_name, item_type])

      cursor = db.execute("SELECT stock FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      final_item_stock = rows[0]['stock']
      print("updated final stock: "+str(final_item_stock))


      cursor = db.execute("SELECT rowid FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      item_id = rows[0][0]

      # insert into decrease table
      cursor = db.execute("INSERT INTO DECREASE(item_id, s_order_id, item_quantity) VALUES(?,?,?)", [item_id, s_order_id, item_quantity])

      cursor = db.execute("SELECT * FROM DECREASE WHERE item_id = ? AND s_order_id = ?", [item_id, s_order_id])
      rows = cursor.fetchall()
      print("create decrease record")
      print("item_id: "+str(rows[0][0])+" s_order_id: "+str(rows[0][1])+" item quantity: "+str(rows[0][2]))

      db.commit()

    return jsonify({"message": "Create sales order success!"})
  else:
    return jsonify({"message": "Content-Type not supported!"})
