# main.py
from fastapi import FastAPI
from src.routers import auth, profile, orders, dashboard
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


app = FastAPI()

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(orders.router)
app.include_router(dashboard.router)