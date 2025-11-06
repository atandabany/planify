from src.models.declarative_base import Base
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Plan(Base):
    __tablename__ = "plan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    hour_volume: Mapped[int] = mapped_column(Integer)
    sms_volume: Mapped[int] = mapped_column(Integer)
    gb_volume: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    type: Mapped[str] = mapped_column(String)


def get_id(self):
    return self.id

def get_name(self):
    return self.name

def get_hour_volume(self):
    return self.hour_volume

def get_sms_volume(self):
    return self.sms_volume

def get_gb_volume(self):
    return self.gb_volume

def get_price(self):
    return self.price

def get_type(self):
    return self.type

def to_string(self):
    return f"{self.id} {self.name} {self.hour_volume} {self.sms_volume} {self.gb_volume} {self.price} {self.type}"
