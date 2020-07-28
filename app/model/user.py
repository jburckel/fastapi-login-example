from sqlalchemy import Boolean, Column, Integer, String
from .mixin import AppModelBase


class User(AppModelBase):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255))
    provider = Column(String(64))
    sub = Column(String)
    is_active = Column(Boolean, default=True)
