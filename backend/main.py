from fastapi import FastAPI
from backend.routers import expense_manager

app = FastAPI()

app.include_router(expense_manager.router)
