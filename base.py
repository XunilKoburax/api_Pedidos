from fastapi  import FastAPI
from pydantic import BaseModel
from datetime import datetime

app  =  FastAPI()

@app.home("/")
def home():
    return "Welcome to orders API"

class person(BaseModel):
    id = int
    name = str
    phone = int
    email = str
    
class product(BaseModel):
    id = int
    description = str
    cost = float
    remaining = float
    total_cost = float
    level_school = str

class order():
    id = int
    id_product = int
    id_person = int

class payment(BaseModel):
    id = int
    id_order= int
    payment = float
    pay_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

