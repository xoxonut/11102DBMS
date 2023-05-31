# 11102DBMS

`flask --app flaskr run --debug`


## API
- staff : CRUD
- supplier : CRUD
- member : CRUD
- purchase order : CRUD
    - increase : CRUD
    - item C U
- sales order : CRUD
    - customer : C R
    - item : R U D
    - decrease : CRUD
- item : UR 

### http verb
- C -> POST
- R -> GET
- U -> PUT
- D -> DELETE

## LIST

**沒寫respond的話就是回傳msg : str**

## staff

- C 
    - request 
        - name : str
        - manager_id : int

- R 
    - respond
        - staffs : list[staff]
- U 
    - request
        - id : int
        - name : str
        - manager_id : int

- D 
    - request
        - id : int


## supplier

- C 
    - request
        - name : str
        - email : str
        - phone : str
        - address : str
- R
    - respond 
        - suppliers : list[supplier]
- U
    - request
        - id : int
        - name : str
        - email : str
        - phone : str
        - address : str
- D
    - request
        - id : int

## member
- C
    - request
        - name : str
        - address : str
        - email : str
        - address : str
- R
    - response
        - members : list[member]
- U
    - request
        - member_id : int
        - name : str
        - address : str
        - email : str
        - address : str
- D
    - request
        - member_id : int

## purchase order

- C
    - request
        - supplier_id : int
        - staff_id : int
        - items : list[item]
```
{
    "supplier_id": 1,
    "staff_id": 2,
    "item_list": [
        {
            "name": "iphone 14",
            "type": "mobile phone",
            "quantity": 3,
            "unit_cost": 50
        },
        {            
            "name": "Mac",
            "type": "test",
            "quantity": 10,
            "unit_cost": 1000
        }
    ]
}
```

- R
    - response
        - orders : json list[purchase order]
 ```
 {
    "p_order_list": [
        {
            "p_order_date": "2023-5-22",
            "p_order_id": 1,
            "staff_name": "Michael",
            "supplier_name": "apple"
        },
        {
            "p_order_date": "2023-5-22",
            "p_order_id": 2,
            "staff_name": "Steve",
            "supplier_name": "tesla"
        },
        {
            "p_order_date": "2023-5-23",
            "p_order_id": 3,
            "staff_name": "John",
            "supplier_name": "tsmc"
        }
       ]
    }
```
- D
    - request
        - p_order_id : int
 ```
 {
    "p_order_id": 1
}
```
- Read purchase order item detail
    - request
        - p_order_id : int
    - response
        - itemdetail list

## sales order
- C
    - request
        - staff_id : int
        - customer_id : int
        - deliver_date : datetime
        - status : bool
        - items : list[item]
- R
    - response
        - orders : list[sales order]

- D
    - request 
        - order_id : str
## Item
- R
    - items : list[item]
- U
    - requerst
        - item_id : int
        - price : int

# 分工
- 前端 2
    - route
    - figma
- 後端 4 
    - **進貨**
    - **出貨**
    - member
      - staff
      - supplier
   - item
      - 建DB
