from dotenv import load_dotenv
import logging
import os

load_dotenv()  # Load from .env

class Settings:
    
    class EMAIL:
        FROM: str = os.getenv("EMAIL_FROM")
        PASSWORD: str = os.getenv("PASSWORD")
    
    class STORAGE:
        PATH: str = os.getenv("STORAGE_PATH")
    
    class LITERAL:
        INF: float = float("inf")
        SECTION_CONSTANT_TUPLE: tuple[str] = (
            'limit',
            'expense'
        )
    class LOGGING:
        level: int =  logging.DEBUG
        base_dir: str = "Logs"

settings = Settings()