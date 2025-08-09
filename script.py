from dotenv import load_dotenv
import os

load_dotenv(".env")  # Explicitly specify the path to the .env file

print("DATABASE_USERNAME:", os.getenv("DATABASE_USERNAME"))
print("DATABASE_PASSWORD:", os.getenv("DATABASE_PASSWORD"))
print("DATABASE_HOSTNAME:", os.getenv("DATABASE_HOSTNAME"))
print("DATABASE_PORT:", os.getenv("DATABASE_PORT"))
print("DATABASE_NAME:", os.getenv("DATABASE_NAME"))




