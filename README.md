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
- item : R 

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
        - manager_id : str

- R 
    - respond
        - staffs : list[staff]
- U 
    - request
        - id : str
        - name : str
        - manager_id : str

- D 
    - request
        - id : str


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
        - id : str
        - name : str
        - email : str
        - phone : str
        - address : str
- D
    - request
        - id : str

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
        - member_id : str
        - name : str
        - address : str
        - email : str
        - address : str
- D
    - request
        - member_id : str

## purchase order

- C
    - request
        - supplier_id : str
        - staff_id : str
        - items : list[item]

- R
    - response
        - orders : json list[purchase order]
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

- D
    - request
        - p_order_id : str

## sales order
- C
    - request
        - staff_id : str
        - customer_id : str
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
