from fastapi import APIRouter, Depends, HTTPException
from src.utils.auth import decode_token
from src.models.user import users

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/info", summary="Profile Info")
def profile_info(my_user: dict = Depends(decode_token)):
    return {"message": f"Profile info for {my_user['username']}"}

@router.put("/update", summary="Update Profile")
def update_profile(my_user: dict = Depends(decode_token), new_email: str = None):
    if new_email:
        users[my_user["username"]]["email"] = new_email
        return {"message": f"Profile updated with new email: {new_email}"}
    raise HTTPException(status_code=400, detail="Email is required for update")

@router.post("/create", summary="Create New Profile")
def create_profile(new_user: dict):
    username = new_user["username"]
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[username] = new_user
    return {"message": f"Profile created for {username}"}

@router.delete("/delete", summary="Delete Profile")
def delete_profile(my_user: dict = Depends(decode_token)):
    del users[my_user["username"]]
    return {"message": f"Profile for {my_user['username']} deleted"}