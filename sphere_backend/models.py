from django.db import models



from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_config import Base
import enum

class LineItem(Base):
    __tablename__ = "line_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    name = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    currency = Column(String)
    discount = Column(Float, default=0.0)
    discount_type = Column(String, default="")
    taxable = Column(Boolean, default=False)
    total_after_discount = Column(Float)

    transaction = relationship("Transaction", back_populates="line_items")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    country = Column(String)
    city = Column(String)
    state = Column(String)
    street = Column(String)
    postal_code = Column(String)

    transaction = relationship("Transaction", back_populates="address")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    line_items = relationship("LineItem", back_populates="transaction")
    address = relationship("Address", uselist=False, back_populates="transaction")
    tax_rate = Column(Float)
    taxable_amount = Column(Float)
    tax_amount = Column(Float)
    total_txn_amount = Column(Float)


class TaxLiability(Base):
    __tablename__ = "tax_liability"

    id = Column(Integer, primary_key=True, index=True)
    tax = Column(Float)

    