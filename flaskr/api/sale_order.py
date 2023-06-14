from flask import Blueprint, jsonify, request
from flaskr.db import get_db
import datetime

bp = Blueprint('sale_order', __name__, url_prefix='/sale_order')

@bp.route('/', methods=['DELETE'])
def delete_sales_order():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
      s_order_id = request.json.get('s_order_id')
      # check order exist
      db = get_db()
      cursor = db.execute("SELECT COUNT(*) AS result FROM SALES_ORDER WHERE rowid=?", [s_order_id])
      rows = cursor.fetchall()
      if (rows[0]['result'] != 1):
        return {"message": "The sales order doesn't exist!"}
      
      cursor = db.execute("SELECT item_id, item_quantity FROM DECREASE WHERE s_order_id=?", [s_order_id])
      rows = cursor.fetchall()
      for row in rows:
        item_id = row[0]
        item_quantity = row[1]
        # increase stock of item
        cursor = db.execute("SELECT stock FROM ITEM WHERE rowid=?", [item_id])
        results = cursor.fetchall()
        initial_item_stock = results[0]['stock']
        new_item_stock = initial_item_stock + item_quantity
        cursor = db.execute("UPDATE ITEM SET stock = ? WHERE rowid=?", [new_item_stock, item_id])

      # delete decrease
      cursor = db.execute("DELETE FROM DECREASE WHERE s_order_id=?", [s_order_id])

      # delete order
      cursor = db.execute("DELETE FROM SALES_ORDER WHERE rowid=?", [s_order_id])

      db.commit()
      return jsonify({"message": "Delete sales order success!"})

    else:
      return jsonify({"message": "Content-type not supported!"})

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
    s_order_date = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor = db.execute("""INSERT INTO SALES_ORDER( staff_id, member_id, s_order_date) 
      VALUES (?,?,?)""", [ staff_id, member_id, s_order_date]) 

    cursor = db.execute("SELECT rowid FROM SALES_ORDER WHERE staff_id = ? AND member_id = ? AND s_order_date=?", [staff_id, member_id, s_order_date])
    rows = cursor.fetchall()
    s_order_id = rows[0][0]
    
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
      new_item_stock = initial_item_stock - int(item_quantity)
      cursor = db.execute("UPDATE ITEM SET stock = ? WHERE name = ? AND type = ?", [new_item_stock, item_name, item_type])


      cursor = db.execute("SELECT rowid FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      item_id = rows[0][0]

      # insert into decrease table
      cursor = db.execute("INSERT INTO DECREASE(item_id, s_order_id, item_quantity) VALUES(?,?,?)", [item_id, s_order_id, item_quantity])


    db.commit()
    db.close()

    return jsonify({"message": "Create sales order success!"})
  else:
    return jsonify({"message": "Content-Type not supported!"})

@bp.route('/detail', methods = ['GET'])
def read_sales_order_detail():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    s_order_id = request.json.get('s_order_id')
    # check if sales order exist
    db = get_db()
    cursor = db.execute("SELECT COUNT(*) AS result FROM SALES_ORDER WHERE rowid=?", [s_order_id])
    rows = cursor.fetchall()
    if (rows[0]['result'] != 1):
      return {"message": "This sales order doesn't exist!"}
    
    # query from decrease JOIN Item
    cursor = db.execute("""
        SELECT IT.unit_price, DCE.item_quantity, IT.name, IT.type 
        FROM DECREASE DCE, ITEM IT
        WHERE DCE.item_id = IT.rowid AND DCE.s_order_id = ?""", [s_order_id])
    rows = cursor.fetchall()

    item_list = []
    for row in rows:
      unit_price = row['unit_price']
      item_quantity = row['item_quantity']
      item_name = row['name']
      item_type = row['type']
      print("name: "+item_name+" type: "+item_type+" quantity: "+str(item_quantity)+" unit_price: "+str(unit_price))
      item = {
        "item_name": item_name,
        "item_type": item_type,
        "item_quantity": item_quantity,
        "unit_price": unit_price
      }
      item_list.append(item)

    db.close()

    return jsonify({"item_list": item_list}) 
  else:
    return jsonify({"message": "Content-Type not supported!"})
