from fastapi  import FastAPI
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import Body, Query, Path
from enum import Enum



app  =  FastAPI()

class person(BaseModel):
    id: Optional[int] = Query(
        ...,
        gt=0
    )
    name : Optional[str] = Query(
        ...,
        min_length =3, 
        max_length = 50,
        title="Person Name"
    )
    phone : Optional[str] = Query(
        ..., 
        min_length = 10,
        max_length = 10,
        title="Phone number"
        )
    email : EmailStr
class categorias(Enum):
    Primaria = "Primaria"
    Secundaria_t = "Secundaria Tecnica"
    cbta = "CBTa"
    
class product(BaseModel):
    id : Optional[int] = Field(
        ...,
        title="id",
        gt=0
    )
    description : Optional[str] = Field(
        ...,
        title="Description",
        min_length=3,
        max_length=50
        )
    cost : Optional[int] =Field(
        ...,
        title="Cost",
        gt=0
    )
    categoria : Optional[categorias] = Field(default = None)


class Order(BaseModel):
    id : int
    id_product : list
    id_person : int

class payment(BaseModel):
    id : Optional[int] = Field(
        title="id",
        description="payment id",
        gt=0, 
        default= None
    )
    id_order: Optional[int] = Field(
        title="id_order",
        description="Order id",
        ge=0, 
        default= None
    )
    payment : Optional[int] = Field(
        title="payment",
        description="payment $$",
        gt=0, 
        default= None
    )
    remaining : Optional[int] =Field(
        ...,
        title="Remaining",
        ge=0
    )
    total_cost : Optional[int] =Field(
        ...,
        title="Total",
        ge=0
    )
    pay_date : Optional[datetime] = Field(
        ...,
        title="datetime",
        description="Transaction Time Stamp",
        ) 

@app.get("/")
def home():
    return "Welcome to orders API"

@app.post("/create_person")
def create_person(Person : person = Body(...)):
    #Commit the person in DB
    return f"Person {Person.name} has been created"

@app.post("/add_product")
def create_product(Product : product = Body(...)):
    #Commit the product in DB
    return f"Product {Product.description} has been created"

@app.post("/add_order")
def create_order(Order : Order= Body(...)):
    #Create order

    #Get Product list

    #Add product list
    
    return f"Your order id is: {Order.id}"



@app.post("/addOrder/")
def add_order(
    Person :  person = Body(...),
    Product : product = Body(...),
    GetOrder : Order = Body(...),
    Payment : payment = Body(...)
    ):
    order = {
        "id": Person.id,
        "id_product": Product.id,
        "id_Order" : GetOrder.id,
        "id_Payment" : Payment.id
        
    }
    return order
    

