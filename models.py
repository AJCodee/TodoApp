# Models for the tables that will show in Database.

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey 

class Todos(Base):
    __tablename__ = 'Todos'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)