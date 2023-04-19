#!/usr/bin/python3
"""This is the review class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey,

class City(BaseModel, Base):	
    """This is the class for review
    Attributes:
        text:
        place_id:
        user_id:
    """
__tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

