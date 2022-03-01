import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db = create_engine("postgresql://" + os.getenv("DATABASE_URL"))