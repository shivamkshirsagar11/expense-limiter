from dotenv import load_dotenv
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

settings = Settings()