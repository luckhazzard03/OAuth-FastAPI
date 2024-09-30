from fastapi import FastAPI, Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt
from decouple import config

app = FastAPI()

# Define el esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

JWT_SECRET_KEY = config('JWT_SECRET_KEY')

# Base de datos ficticia de usuarios
users = {
    "Angel": {"username": "Angel", "email": "eduar19311@hotmail.com", "password": "BuckAslam27"},
    #"Emmanuel": {"username": "Emmanuel", "email": "Emmanuel19311@hotmail.com", "password": "BuckAslam28"},
}

# Función para codificar el token JWT
def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token

# Función para decodificar el token y verificar el usuario
def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    user = users.get(data["username"])
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Ruta para autenticación
@app.post("/auth", summary="User Authentication")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}


# ---- Modulo Profile ---- #
profile_router = APIRouter(tags=["Profile"])

@profile_router.get("/info", summary="Profile Info")
def profile_info(my_user: dict = Depends(decode_token)):
    return {"message": f"Profile info for {my_user['username']}"}

@profile_router.put("/update", summary="Update Profile")
def update_profile(my_user: dict = Depends(decode_token), new_email: str = None):
    if new_email:
        users[my_user["username"]]["email"] = new_email
        return {"message": f"Profile updated with new email: {new_email}"}
    raise HTTPException(status_code=400, detail="Email is required for update")

@profile_router.post("/create", summary="Create New Profile")
def create_profile(new_user: dict):
    username = new_user["username"]
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[username] = new_user
    return {"message": f"Profile created for {username}"}

@profile_router.delete("/delete", summary="Delete Profile")
def delete_profile(my_user: dict = Depends(decode_token)):
    del users[my_user["username"]]
    return {"message": f"Profile for {my_user['username']} deleted"}

app.include_router(profile_router, prefix="/profile", dependencies=[Depends(decode_token)])


# ---- Modulo Orders ---- #
orders_router = APIRouter(tags=["Orders"])

@orders_router.get("/list", summary="List Orders")
def list_orders(my_user: dict = Depends(decode_token)):
    return {"message": f"List of orders for {my_user['username']}"}

@orders_router.post("/create", summary="Create Order")
def create_order(order_details: dict, my_user: dict = Depends(decode_token)):
    return {"message": f"Order created for {my_user['username']}", "order": order_details}

@orders_router.put("/update/{order_id}", summary="Update Order")
def update_order(order_id: int, updated_details: dict, my_user: dict = Depends(decode_token)):
    return {"message": f"Order {order_id} updated for {my_user['username']}", "details": updated_details}

@orders_router.delete("/delete/{order_id}", summary="Delete Order")
def delete_order(order_id: int, my_user: dict = Depends(decode_token)):
    return {"message": f"Order {order_id} deleted for {my_user['username']}"}

app.include_router(orders_router, prefix="/orders", dependencies=[Depends(decode_token)])


# ---- Modulo Dashboard ---- #
dashboard_router = APIRouter(tags=["Dashboard"])

@dashboard_router.get("/overview", summary="Dashboard Overview")
def dashboard_overview(my_user: dict = Depends(decode_token)):
    return {"message": f"Dashboard overview for {my_user['username']}"}

@dashboard_router.post("/create", summary="Create Dashboard Widget")
def create_dashboard_widget(widget_data: dict, my_user: dict = Depends(decode_token)):
    return {"message": f"Dashboard widget created for {my_user['username']}", "widget": widget_data}

@dashboard_router.put("/update/{widget_id}", summary="Update Dashboard Widget")
def update_dashboard_widget(widget_id: int, widget_data: dict, my_user: dict = Depends(decode_token)):
    return {"message": f"Dashboard widget {widget_id} updated for {my_user['username']}", "widget": widget_data}

@dashboard_router.delete("/delete/{widget_id}", summary="Delete Dashboard Widget")
def delete_dashboard_widget(widget_id: int, my_user: dict = Depends(decode_token)):
    return {"message": f"Dashboard widget {widget_id} deleted for {my_user['username']}"}

app.include_router(dashboard_router, prefix="/dashboard", dependencies=[Depends(decode_token)])
