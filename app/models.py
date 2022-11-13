from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class user(Base):

    __tablename__ = "users"

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))
    id = Column(Integer, primary_key = True , nullable = False)
    email = Column(String , nullable = False, unique = True)
    password = Column(String, nullable = False)
    is_admin = Column(Boolean, server_default= "False",nullable = False, )

class votes(Base):

    __tablename__ = "voters"

    epic_no = Column(String, nullable = False, primary_key = True)
    name = Column(String, nullable = False)
    age = Column(Integer, nullable = False)
    father_name = Column(String, server_default= None)
    husband_name = Column(String, server_default= None)
    sex = Column(String)
    house_no = Column(String, nullable = False)
    poll_booth = Column(Integer, nullable = False)
    district = Column(String, nullable = False)
    state = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))
