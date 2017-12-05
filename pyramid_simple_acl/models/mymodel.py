from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Date,
    ForeignKey,
)

from .meta import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class TblRole(Base):
    __tablename__ = "tbl_role"
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False)
    role_order = Column(Integer, nullable=False)
    role_description = Column(Text, nullable=False)

    def __init__(self, role_name, role_order, role_description):
        self.role_name = role_name
        self.role_order = role_order
        self.role_description = role_description


class TblRoom(Base):
    __tablename__ = "tbl_room"
    room_number = Column(Integer, primary_key=True, nullable=False)
    room_type = Column(String(6), nullable=False)
    room_floor = Column(Integer, nullable=False)
    room_is_reserved = Column(Integer, nullable=False)

    def __init__(self, room_number, room_type, room_floor, room_is_reserved):
        self.room_number = room_number
        self.room_type = room_type
        self.room_floor = room_floor
        self.room_is_reserved = room_is_reserved

class TblUser(Base):
    __tablename__ = "tbl_user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), nullable=False)
    user_password = Column(String(128), nullable=False)
    user_is_login = Column(Integer, nullable=False)
    # role_id = Column(Integer, nullable=False)
    role_id = Column(Integer, ForeignKey('tbl_role.role_id'))
    role = relationship('TblRole', backref='userrole')

    def __init__(self, user_name, user_password, user_is_login, role):
        self.user_name = user_name
        self.user_password = user_password
        self.user_is_login = user_is_login
        self.role = role

class TblReservation(Base):
    __tablename__ = "tbl_reservation"
    reserv_id = Column(Integer, primary_key=True, autoincrement=True)
    # room_number = Column(Integer, nullable=False)
    reserve_start_date = Column(Date, default=func.timezone('UTC', func.current_timestamp()), nullable=False)
    reserve_end_date = Column(Date, nullable=False)
    # cust_id = Column(Integer, nullable=False)
    room = relationship('TblRoom', backref='reserveroom')
    room_number = Column(Integer, ForeignKey('tbl_room.room_number'))
    
    cust_id = Column(Integer, ForeignKey('tbl_customer.cust_id'))
    cust = relationship('TblCustomer', backref='reservecust')

    def __init__(self, reserve_start_date, reserve_end_date, room, cust):
        self.reserve_start_date = reserve_start_date
        self.reserve_end_date = reserve_end_date
        self.room = room
        self.cust = cust

    
class TblCustomer(Base):
    __tablename__ = "tbl_customer"
    cust_id = Column(Integer, primary_key=True, autoincrement=True)
    cust_first_name = Column(String(50), nullable=False)
    cust_last_name = Column(String(50), nullable=False)
    cust_address = Column(Text, nullable=False)
    cust_phone = Column(String(25), nullable=False)
    cust_profile = Column(String(4), nullable=False)

    def __init__(self, cust_first_name, cust_last_name, cust_address, cust_phone, cust_profile):
        self.cust_first_name = first_name
        self.cust_last_name = cust_last_name
        self.cust_address = cust_address
        self.cust_phone = cust_phone
        self.cust_profile = cust_profile

"""
class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


Index('my_index', MyModel.name, unique=True, mysql_length=255)
"""