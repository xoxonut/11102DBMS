# 11102DBMS

## Steps to create ERP System web page

- Install virtual environment:
  `pip3 install virtualenv`
- Create env file:
  `virtualenv env`
- Activate virtual environment:
  - In Windows Powershell:
    `.\env\Scripts\activate.ps1`
  - In Windows CMD:
    `.\venv\Scripts\activate.bat`
  - In Linux / MacOS:
    `source ./venv/bin/activate`
- Install flask:
  `pip3 install flask`
- Install requests
  `pip install requests`
- Create Database:
  `python schema.py`
- Run the app:
  `flask --app flaskr run --debug`
- login page
  account: `erp123`
  password: `erp456`

## API

- staff : CRUD
- supplier : CRUD
- member : CRUD
- purchase order : CRUD
  - increase : CRUD
  - item C U
- sales order : CRUD
  <<<<<<< HEAD - customer : C R - item : R U D - decrease : CRUD
- # item : UR
  - customer : C R
  - item : R U D
  - decrease : CRUD
- item : R
  > > > > > > > feature/db_and_item_api

### http verb

- C -> POST
- R -> GET
- U -> PUT
- D -> DELETE

## LIST

**沒寫 respond 的話就是回傳 msg : str**

## staff

<<<<<<< HEAD

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
      "entry_date": "2023-5-20",
      "manager_id": "NULL",
      "name": "John",
      "staff_id": 1
    },
    {
      "entry_date": "2023-5-21",
      "manager_id": 1,
      "name": "Michael",
      "staff_id": 2
    },
    {
      "entry_date": "2023-5-21",
      "manager_id": 1,
      "name": "Steve",
      "staff_id": 3
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

### C

- request
  - name : str
  - email : str
  - phone : str
  - address : str

```json
{
  "name": "Test",
  "email": "test@test.com",
  "phone_number": "0123456789",
  "address": "Taipei"
}
```

- respond

```json
{
  "message": "Supplier created successfully!",
  "supplier_id": 4
}
```

### R

- respond
  - suppliers : list[supplier]

```json
{
  "supplier_list": [
    {
      "address": "Cupertino, California, United States",
      "email": "apple@apple.com",
      "name": "apple",
      "phone_number": "1234567890",
      "supplier_id": 1
    },
    {
      "address": "Austin, Texas, United States",
      "email": "tesla@tesla.com",
      "name": "tesla",
      "phone_number": "9876543210",
      "supplier_id": 2
    },
    {
      "address": "8, Li-Hsin Rd. 6, Hsinchu Science Park,Hsinchu 300-096, Taiwan, R.O.C.",
      "email": "tsmc@tsmc.com",
      "name": "tsmc",
      "phone_number": "1357924680",
      "supplier_id": 3
    }
  ]
}
```

### U

- request
  - id : int
  - name : str
  - email : str
  - phone : str
  - address : str

```json
{
  "supplier_id": 4,
  "name": "NewTest",
  "email": "test@test.com.tw",
  "phone_number": "9123456789",
  "address": "NTTaipei"
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
  "supplier_id": 4
}
```

- respond

```json
{
  "message": "Supplier deleted successfully"
}
```

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
      "address": "singapore",
      "email": "tom@gmail.com",
      "member_id": 1,
      "name": "Tom",
      "phone_number": "1122334455"
    },
    {
      "address": "usa",
      "email": "emma@gmail.com",
      "member_id": 2,
      "name": "Emma",
      "phone_number": "6677889900"
    },
    {
      "address": "thailand",
      "email": "jack@gmail.com",
      "member_id": 3,
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
  "member_id": 4
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

- request: url: /purchase_order/detail
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

### C

- request
  - staff_id : int
  - customer_id : int
  - deliver_date : datetime
  - status : bool
  - items : list[item]

```json
{
  "member_id": 1,
  "staff_id": 2,
  "item_list": [
    {
      "name": "iphone 14",
      "type": "mobile phone",
      "quantity": 2
    },
    {
      "name": "M2",
      "type": "chip",
      "quantity": 3
    }
  ]
}
```

- respond

```json
{
  "message": "Create sales order success!"
}
```

### R

- response
  - orders : list[sales order]

```json
{
  "s_order_list": [
    {
      "member_name": "Tom",
      "s_order_date": "2023-5-24",
      "s_order_id": 1,
      "staff_name": "Michael"
    },
    {
      "member_name": "Jack",
      "s_order_date": "2023-5-24",
      "s_order_id": 2,
      "staff_name": "Michael"
    },
    {
      "member_name": "Tom",
      "s_order_date": "2023-5-25",
      "s_order_id": 3,
      "staff_name": "Steve"
    }
  ]
}
```

### D

- request
  - order_id : str

```json
{
  "s_order_id": 4
}
```

- respond

```json
{
  "message": "Delete sales order success!"
}
```

### read sales order detail of item

- request: url: /sale_order/detail
  - s_order_id: int

```json
{
  "s_order_id": 4
}
```

- respond

```json
{
  "item_list": [
    {
      "item_name": "iphone 14",
      "item_quantity": 2,
      "item_type": "mobile phone",
      "unit_price": 100
    },
    {
      "item_name": "M2",
      "item_quantity": 3,
      "item_type": "chip",
      "unit_price": 100
    }
  ]
}
```

## Item

### R

- respond
  - items : list[item]

```json
{
  "item_list": [
    {
      "item_id": 1,
      "name": "iphone 14",
      "stock": 10,
      "type": "mobile phone",
      "unit_price": 100
    },
    {
      "item_id": 2,
      "name": "model x",
      "stock": 5,
      "type": "car",
      "unit_price": 1000
    },
    {
      "item_id": 3,
      "name": "M2",
      "stock": 50,
      "type": "chip",
      "unit_price": 100
    },
    {
      "item_id": 4,
      "name": "Mac",
      "stock": 0,
      "type": "test",
      "unit_price": null
    }
  ]
}
```

### U

- requerst
  - item_id : int
  - price : int

```json
{
  "item_id": 1,
  "unit_price": 100
}
```

- respond

```json
{
  "message": "Item updated successfully"
}
```

## 列出一段時間的營業額

### R

- request: url: /income
  - month: str
  - year: str

```json
{
  "month": "Jun",
  "year": "2023"
}
```

- respond:

```json
{
  "income": 500
}
```

## 列出每位員工在一段時間內的業績

### R

- request: url: /staff_performance
- month: str
- year: str

```json
{
  "month": "Jun",
  "year": "2023"
}
```

- respond:

```json
{
  "performance_list": [
    {
      "name": "John",
      "performance": 1200
    },
    {
      "name": "Michael",
      "performance": 500
    },
    {
      "name": "Steve",
      "performance": 1300
    }
  ]
}
```

=======

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
    - delivery_date : datetime
    - status : bool
- R
  - response
    - orders : list[purchase order]
- U
  - request
    - order_id : str
    - status : bool
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
- U
  - request
    - order_id : str
    - status : bool
- D
  - request
    - order_id : str

## Item

- R
  - items : list[item]

> > > > > > > feature/db_and_item_api

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
    - 建 DB
