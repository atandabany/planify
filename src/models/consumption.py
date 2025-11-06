from src.models.declarative_base import Base
import datetime
from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Consumption(Base):
    __tablename__ = "consumption"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    date: Mapped[datetime.date] = mapped_column(Date)
    hour_volume: Mapped[float] = mapped_column(Float)
    sms_volume: Mapped[int] = mapped_column(Integer)
    gb_volume: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="consumption_history")


    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name  
    
    def get_date(self):
        return self.date
    
    def get_hour_volume(self):  
        return self.hour_volume 
    
    def get_sms_volume(self):   
        return self.sms_volume
    
    def get_gb_volume(self):
        return self.gb_volume   
    
    def get_price(self):    
        return self.price
    
    def to_string(self):
        return f"{self.id} {self.name} {self.date} {self.hour_volume} {self.sms_volume} {self.gb_volume} {self.price}"
    
    