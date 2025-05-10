from fastapi import FastAPI
from routers import expense_manager
import os
from utils.logger import create_logger

LOGGER = create_logger(os.path.basename(__file__))

LOGGER.info("Creating FastAPI app...")
app = FastAPI()

LOGGER.info("Adding expense_manager.router in app")
app.include_router(expense_manager.router)
