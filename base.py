from fastapi  import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Body, Query, Path
from enum import Enum
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError
import jwt


app  =  FastAPI()

#Configuracion de jwt
SECRET_KEY = "secret"  
ALGORITHM = "HS256"  
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer("/login_tocken")

 

#Definition auth function
def create_jwt_token(data: dict, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM, expiration: int = 3600):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

#Create Auth function
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
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

#test dictionary get an authentication
fake_db = {
    "Test":{
        "username":"Test",
        "password":"test"
    }
}
class users(BaseModel): 
    username: Optional[str]=Query(default=None, min_length=3, max_length=15)
    password: Optional[str]=Query(default=None, min_length=2, max_length=30)
 

@app.get("/")
def home():
    return "Welcome to orders API"

@app.post("/login_tocken")
def login(form_data : OAuth2PasswordRequestForm = Depends()):
    if not form_data.username:
        raise HTTPException (status_code=401, 
                             detail="Not valid authenticate" ,
                             headers={"WWW-Authenticate":"Bearier"})
    if form_data.username == fake_db["Test"]["username"] and\
        fake_db["Test"]["password"] == form_data.password:
        print("Entre")
        token = create_jwt_token({"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    else:
        print("No entre")
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.post("/create_person")
def create_person(Person : person = Body(...)):
    #Commit the person in DB
    return f"Person {Person.name} has been created"

@app.post("/add_product")
def create_product(Product : product = Body(...),
                    current_user: dict = Depends(oauth2_scheme)):
    #Commit the product in DB
    return f"Product {Product.description} has been created by user {current_user['sub']}"


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


    

