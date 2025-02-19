from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey
from app.database import Base
import datetime
from sqlalchemy.orm import relationship

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True, nullable=False)
    amount = Column(Float, index=True, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, index=True, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id')) 

    user = relationship("User", back_populates="expenses")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    expenses = relationship("Expense", back_populates="user")