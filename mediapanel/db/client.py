# pylint: disable=missing-docstring

from sqlalchemy import Column, Integer, String

from .base import Base


class Client(Base):  # pylint: disable=too-few-public-methods,missing-docstring
    __tablename__ = "clients"
    client_id = Column("clientID", Integer, primary_key=True)
    client_name = Column("clientName", String)
    first_name = Column("firstName", String)
    last_name = Column("lastName", String)
    email = Column(String, nullable=False, unique=True)
    address = Column(String)
    city = Column(String)
    zipcode = Column(String)
    timezone = Column(String)
    country = Column(String)
    state = Column(String)
    uuid = Column(String(36))
