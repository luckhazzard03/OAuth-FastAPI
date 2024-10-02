from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.auth import decode_token, encode_token
from src.models.user import users

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/auth", summary="Orders Authentication")
def orders_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/list", summary="List Orders")
def list_orders(my_user: dict = Depends(decode_token)):
    return {"message": f"List of orders for {my_user['username']}"}

@router.post("/create", summary="Create Order")
def create_order(order_details: dict, my_user: dict = Depends(decode_token)):
    return {"message": f"Order created for {my_user['username']}", "order": order_details}

@router.put("/update/{order_id}", summary="Update Order")
def update_order(order_id: int, updated_details: dict, my_user: dict = Depends(decode_token)):
    return {"message": f"Order {order_id} updated for {my_user['username']}", "details": updated_details}

@router.delete("/delete/{order_id}", summary="Delete Order")
def delete_order(order_id: int, my_user: dict = Depends(decode_token)):
    return {"message": f"Order {order_id} deleted for {my_user['username']}"}