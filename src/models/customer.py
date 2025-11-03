from src.models.declarative_base import Base
from src.models.consumption import Consumption
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_name: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    current_plan: Mapped[str] = mapped_column(String) 
    consumption_history: Mapped[list["Consumption"]] = relationship(back_populates="customer")


    def get_id(self):
            return self.id
        
    def get_last_name(self):
        return self.last_name
        
    def get_first_name(self):
        return self.first_name

    def get_email(self):
        return self.email

    def get_current_plan(self):
        return self.current_plan

    def get_consumption_history(self):
         history = []
         for consumption in self.consumption_history:
            history.append(consumption.to_string())
            return history
         
    def to_string(self):
        return f"{self.id} {self.last_name} {self.first_name} {self.email} {self.current_plan} {self.consumption_history}"