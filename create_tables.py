# create_tables.py

from sqlalchemy import create_engine
from sqlalchemy_config import Base
from sphere_backend.models import Transaction, LineItem, Address

DATABASE_URL = "postgresql+psycopg://postgres:test@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(bind=engine)
