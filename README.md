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

### C 
   - request 
        - name : str
        - manager_id : int
```json
{
    "manager_id": 2,
    "name": "Test"

}
```
 - respond
```json
{
    "message": "Staff member created successfully!",
    "staff_id": 4
}
```
### R 
   - respond
        - staffs : list[staff]
```json
{
    "staff_list": [
        {
            "entry_date": "2023-05-20",
            "manager_id": 2,
            "name": "John"
        },
        {
            "entry_date": "2023-05-21",
            "manager_id": 1,
            "name": "Michael"
        },
        {
            "entry_date": "2023-05-21",
            "manager_id": 1,
            "name": "Steve"
        }
    ]
}
```
### U 
   - request
        - id : int
        - name : str
        - manager_id : int
```json
{
    "manager_id": 1,
    "staff_id": 4,
    "name": "NewTest"

}
```
 - respond
```json
{
    "message": "Staff member updated successfully!"
}
```
### D 
   - request
        - id : int
```json
{
    "staff_id": 4

}
```
 - respond
```json
{
    "message": "Staff member deleted successfully!"
}
```

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
### C
   - request
        - name : str
        - address : str
        - email : str
        - address : str
```json
{
    "name": "Test",
    "email": "test@test.com",
    "phone_number": "1234567890",
    "address": "Taipei"

}
```
- response
```json
{
    "member_id": 4,
    "message": "Member created successfully!"
}
```
### R
   - response
        - members : list[member]
```json
{
    "member_list": [
        {
            "address": "nccu",
            "email": "tom@gmail.com",
            "name": "Tom",
            "phone_number": "1122334455"
        },
        {
            "address": "singapore",
            "email": "emma@gmail.com",
            "name": "Emma",
            "phone_number": "6677889900"
        },
        {
            "address": "thailand",
            "email": "jack@gmail.com",
            "name": "Jack",
            "phone_number": "5544332211"
        }
    ]
}
```
### U
   - request
        - member_id : int
        - name : str
        - address : str
        - email : str
        - address : str
```json
{
    "member_id": 4,
    "name": "newTest",
    "email": "test@test.com.tw",
    "phone_number": "1234567899",
    "address": "NewTaipei"

}
```
 - response
```json
{
    "message": "Member updated successfully!"
}
```
### D
   - request
        - member_id : int
```json
{
    "member_id":4
}
```
 - response
```json
{
    "message": "Member deleted successfully!"
}
```

## purchase order

### C
   - request
        - supplier_id : int
        - staff_id : int
        - items : list[item]
```json
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
  - response
```json
{
    "message": "Create purchase order success!"
}
```
    
 ### R
   - response
        - orders : json list[purchase order]
 ```json
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
### D
   - request
        - p_order_id : int
 ```json
 {
    "p_order_id": 1
}
```
   - response
```json
{
    "message": "Delete purchase order success!"
}
```
### Read purchase order item detail
   - request
        - p_order_id : int
```json
{
    "p_order_id": 55583
}
```

   - response
        - item_detail list
      
```json
{
    "item_list": [
        {
            "item_name": "iphone 14",
            "item_quantity": 3,
            "item_type": "mobile phone",
            "unit_cost": 50
        },
        {
            "item_name": "Mac",
            "item_quantity": 10,
            "item_type": "test",
            "unit_cost": 1000
        }
    ]
}
```

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
