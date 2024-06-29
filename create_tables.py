# create_tables.py
import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy_config import Base
from sphere_backend.models import Transaction, LineItem, Address

engine = create_engine(os.getenv('DB_URL'))

# Create all tables
Base.metadata.create_all(bind=engine)
