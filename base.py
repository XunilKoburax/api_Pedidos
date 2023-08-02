from fastapi  import FastAPI
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import Body, Query, Path
from enum import Enum



app  =  FastAPI()

class person(BaseModel):
    id: int = Field(
        gt=0
    )
    name : str = Field(
        ...,
        min_length =3, 
        max_length = 50,
        title="Person Name",
        examples="Maria"
    )
    phone : str = Field(
        ..., 
        min_length = 10,
        max_length = 10,
        title="Phone number",
        examples="2345678910"
        )
    email : Optional[EmailStr] = Field (
        title="email",
        examples="example@example.com"
    )
class categorias(Enum):
    Primaria = "Primaria"
    Secundaria_t = "Secundaria Tecnica"
    cbta = "CBTa"
    
class product(BaseModel):
    id : Optional[int] = Field(
        ...,
        title="id",
        gt=0,
    )
    description : str = Field(
        ...,
        title="Description",
        min_length=3,
        max_length=50,
        examples="Pans Secundaria Técnica"
    )
    cost : Optional[float] =Field(
        ...,
        title="Cost",
        gt=0,
        examples="200.00"
    )
    remaining : Optional[float] =Field(
        ...,
        title="Remaining",
        ge=0,
        examples="0.00"
    )
    total_cost : Optional[float] =Field(
        ...,
        title="Total",
        ge=0,
        examples="200.00"
    )
    categoria : Optional[categorias] = Field(default = None)


class order(BaseModel):
    id : int
    id_product : int
    id_person : int

class payment(BaseModel):
    id : Optional[int] = Field(
        title="id",
        description="payment id",
        gt=0,
        examples="0"
    )
    id_order: Optional[int] = Field(
        title="id_order",
        description="Order id",
        gt=0,
        examples="0"
    )
    payment : Optional[float] = Field(
        title="payment",
        description="payment $$",
        gt=0,
        examples="20"
    )
    pay_date : Optional[str] = Field(
        ...,
        title="datetime",
        description="Transaction Time Stamp",
        examples="11-08-2022 14:00:23",
        min_length=19,
        
        ) 

@app.get("/")
def home():
    return "Welcome to orders API"