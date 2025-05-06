from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

class Settings:
    
    class EMAIL:
        FROM: str = os.getenv("EMAIL_FROM")
        PASSWORD: str = os.getenv("PASSWORD")
    
    class STORAGE:
        PATH: str = os.getenv("STORAGE_PATH")

settings = Settings()