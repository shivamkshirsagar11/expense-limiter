from fastapi import FastAPI
from routers import add_section as add_section_router

app = FastAPI()

app.include_router(add_section_router.router)
