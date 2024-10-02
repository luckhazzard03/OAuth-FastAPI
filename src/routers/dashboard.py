from fastapi import APIRouter, Depends
from src.utils.auth import decode_token

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/overview", summary="Dashboard Overview")
def dashboard_overview(my_user: dict = Depends(decode_token)):
    return {"message": f"Dashboard overview for {my_user['username']}"}

@router.post("/create", summary="Create Dashboard Widget")
def create_dashboard_widget(widget_data: dict, my_user: dict = Depends(decode_token)):
    return {"message": f"Dashboard widget created for {my_user['username']}", "widget": widget_data}

@router.put("/update/{widget_id}", summary="Update Dashboard Widget")
def update_dashboard_widget(widget_id: int, widget_data: dict, my_user: dict = Depends(decode_token)):
    return {"message": f"Dashboard widget {widget_id} updated for {my_user['username']}", "widget": widget_data}

@router.delete("/delete/{widget_id}", summary="Delete Dashboard Widget")
def delete_dashboard_widget(widget_id: int, my_user: dict = Depends(decode_token)):
    return {"message": f"Dashboard widget {widget_id} deleted for {my_user['username']}"}