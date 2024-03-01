from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func


class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    category = Column(String)
    created_at = Column(DateTime, default=func.now())
