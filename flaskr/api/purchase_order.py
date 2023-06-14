from flask import Blueprint, jsonify, request
from flaskr.db import get_db
import datetime

bp = Blueprint('purchase_order', __name__, url_prefix='/purchase_order')

@bp.route('/', methods=['GET'])
def read_purchase_order():
  db = get_db()
  cursor = db.execute("""
      SELECT P.rowid AS p_order_id, SP.name AS supplier_name, ST.name AS staff_name, p_order_date
      FROM PURCHASE_ORDER P, SUPPLIER SP, STAFF ST
      WHERE P.supplier_id = SP.rowid AND P.staff_id = ST.rowid""")
  rows = cursor.fetchall()

  item_list=[]
  for row in rows:
    p_order_id, supplier_name,  staff_name, p_order_date = row
    item = {
      "p_order_id": p_order_id,
      "supplier_name": supplier_name,
      "staff_name": staff_name,
      "p_order_date": p_order_date
    }
    item_list.append(item)

  db.close()
  
  return jsonify({"p_order_list": item_list})
  
@bp.route('/', methods=['POST'])
def create_purchase_order():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    supplier_id = request.json.get('supplier_id')
    staff_id = request.json.get('staff_id')
    item_list = request.json.get('item_list')

    # check if staff is exist
    db = get_db()
    cursor = db.execute("SELECT COUNT(*) AS result FROM STAFF WHERE rowid=?", [staff_id])
    rows = cursor.fetchall()
    if (rows[0]['result'] != 1):
      return {"message": "This staff doesn't exist!"}
    
    # check if supplier is exist
    cursor = db.execute("SELECT COUNT(*) AS result FROM SUPPLIER WHERE rowid=?", [supplier_id])
    rows = cursor.fetchall()
    if (rows[0]['result'] != 1):
      return {"message": "This supplier doesn't exist!"}

    # insert into purchase order
    p_order_date = datetime.datetime.now().strftime("%c")
    cursor = db.execute("""INSERT INTO PURCHASE_ORDER(supplier_id, staff_id, p_order_date) 
      VALUES (?,?,?)""", [ supplier_id, staff_id, p_order_date]) 

    cursor = db.execute("SELECT rowid FROM PURCHASE_ORDER WHERE supplier_id = ? AND staff_id = ? AND p_order_date=?", [supplier_id, staff_id, p_order_date])
    rows = cursor.fetchall()
    p_order_id = rows[0][0]

    for item in item_list:
      item_name = item.get('name')
      item_type = item.get('type')
      item_quantity = item.get('quantity')
      item_unit_cost = item.get('unit_cost')

      # check if item's name and type have existted. Otherwise, create item
      cursor = db.execute("SELECT COUNT(*) AS result FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      if (rows[0]['result'] != 1):
        #item doesn't exist, then create item
        cursor = db.execute("INSERT INTO ITEM( name, type, stock) VALUES (?, ?, ?)", [ item_name, item_type, item_quantity]) 
      else:
        # item exist, get item stock then increase item quantity
        cursor = db.execute("SELECT stock FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
        rows = cursor.fetchall()
        initial_item_stock = rows[0]['stock']
        new_item_stock = initial_item_stock + int(item_quantity)
        cursor = db.execute("UPDATE ITEM SET stock = ? WHERE name = ? AND type = ?", [new_item_stock, item_name, item_type])

      cursor = db.execute("SELECT rowid FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      item_id = rows[0][0]

      # insert into increase table
      cursor = db.execute("INSERT INTO INCREASE(item_id, p_order_id, unit_cost, item_quantity) VALUES(?,?,?,?)", [item_id, p_order_id, item_unit_cost, item_quantity])


    db.commit()
    db.close()
      
    return jsonify({"message": "Create purchase order success!"})
  else:
    return jsonify({"message": "Content-Type not supported!"})

@bp.route('/', methods = ['DELETE'])
def delete_purchase_order():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    p_order_id = request.json.get('p_order_id')
    # check if purchase order exist
    db = get_db()
    cursor = db.execute("SELECT COUNT(*) AS result FROM PURCHASE_ORDER WHERE rowid=?", [p_order_id])
    rows = cursor.fetchall()
    if (rows[0]['result'] != 1):
      return {"message": "This purchase order doesn't exist!"}

    # get all related item_id and quantity from increase table
    cursor = db.execute("SELECT item_id, item_quantity FROM INCREASE WHERE p_order_id=?", [p_order_id])
    rows = cursor.fetchall()
    for row in rows:
      item_id = row[0]
      item_quantity = row[1]
      # decrease stock of item
      cursor = db.execute("SELECT stock FROM ITEM WHERE rowid=?", [item_id])
      results = cursor.fetchall()
      initial_item_stock = results[0]['stock']
      new_item_stock = initial_item_stock - item_quantity
      cursor = db.execute("UPDATE ITEM SET stock = ? WHERE rowid=?", [new_item_stock, item_id])

    # delete increase table
    cursor = db.execute("DELETE FROM INCREASE WHERE p_order_id=?", [p_order_id])

    # delete purchase order
    cursor = db.execute("DELETE FROM PURCHASE_ORDER WHERE rowid=?", [p_order_id])

    db.commit()
    db.close()
    return jsonify({"message": "Delete purchase order success!"})

  else:
    return jsonify({"message": "Content-type not supported!"})

@bp.route('/detail', methods = ['GET'])
def read_purchase_order_detail():
  content_type = request.headers.get('Content-Type')
  if (content_type == 'application/json'):
    p_order_id = request.json.get('p_order_id')
    # check if purchase order exist
    db = get_db()
    cursor = db.execute("SELECT COUNT(*) AS result FROM PURCHASE_ORDER WHERE rowid=?", [p_order_id])
    rows = cursor.fetchall()
    if (rows[0]['result'] != 1):
      return {"message": "This purchase order doesn't exist!"}
    
    # query from Increase JOIN Item
    cursor = db.execute("""
        SELECT ICE.unit_cost, ICE.item_quantity, IT.name, IT.type 
        FROM INCREASE ICE, ITEM IT
        WHERE ICE.item_id = IT.rowid AND ICE.p_order_id = ?""", [p_order_id])
    rows = cursor.fetchall()

    item_list = []
    for row in rows:
      unit_cost = row['unit_cost']
      item_quantity = row['item_quantity']
      item_name = row['name']
      item_type = row['type']
      item = {
        "item_name": item_name,
        "item_type": item_type,
        "item_quantity": item_quantity,
        "unit_cost": unit_cost
      }
      item_list.append(item)

    db.close()

    return jsonify({"item_list": item_list}) 
  else:
    return jsonify({"message": "Content-Type not supported!"})
  