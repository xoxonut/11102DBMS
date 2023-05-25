from flask import Blueprint, jsonify, request
from flaskr.db import get_db
import random # this line should delete after DB modified to use rowid

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

    # TODO:insert into purchase order
    db.execute

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
        item_id = random.randint(1000, 100000) # this line should delete after DB modified to rowid
        cursor = db.execute("INSERT INTO ITEM(item_id, name, type, stock) VALUES (?, ?, ?, ?)", [item_id, item_name, item_type, item_quantity])
        db.commit()
        print( "This item doesn't exist!")

      # TODO: insert into increase table
      cursor = db.execute("SELECT rowid FROM ITEM WHERE name = ? AND type = ?", [item_name, item_type])
      rows = cursor.fetchall()
      print("item has existed ")
      print("rowid: "+str(rows[0][0]))


      # increase item
      
    return "ok" 
  else:
    return 'Content-Type not supported!'