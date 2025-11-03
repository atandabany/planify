from src.models.customer import Customer
from src.models.plan import Plan
from src.models.consumption import Consumption
from src.models.declarative_base import Base
import random
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


DATABASE_URL = "mysql+mysqlconnector://root:@localhost/planify"
engine = create_engine(DATABASE_URL, echo=True)


def load_fixtures():

    profiles = [
        {
            "name": "SFR Forfait 2€",
            "price": 5.99, 
            "hour_volume": 1.5, 
            "sms_volume": 120, 
            "gb_volume": 0.8, 
            "variation": 
                {
                    "hour": 0.25, 
                    "sms": 30, 
                    "gb": 0.1
                }
        },
        {
            "name": "SFR Série Free",
            "price": 15.99, 
            "hour_volume": 8.0, 
            "sms_volume": 150, 
            "gb_volume": 15.0, 
            "variation": 
                {
                    "hour": 2.0, 
                    "sms": 50, 
                    "gb": 5.0
                }
        },
        {
            "name": "SFR Forfait Free 5G",
            "price": 17.99, 
            "hour_volume": 12.0, 
            "sms_volume": 200, 
            "gb_volume": 65.0, 
            "variation": 
                {
                    "hour": 3.00, 
                    "sms": 50, 
                    "gb": 10.0
                }
        },
    ]

    customers = [
        Customer(last_name="B.", first_name="Yassine", email="yassine.b@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="B.", first_name="Tasnime", email="tasnime.b@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="C.", first_name="Eren", email="eren.c@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="C.", first_name="Celie", email="celie.c@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="D.", first_name="Barbara", email="barbara.d@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="D.", first_name="Rachel", email="rachel.d@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="D.", first_name="Edgar", email="edgar.d@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="D.", first_name="Ellyne", email="ellyne.d@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="G.", first_name="Lucie", email="lucie.g@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="H.", first_name="Omega", email="omega.h@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="H.", first_name="Carolina", email="carolina.h@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="H.", first_name="Meriem", email="meriem.h@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="I.", first_name="Anis", email="anis.i@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="K.", first_name="Sabera", email="sabera.k@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="L.", first_name="Pierre", email="pierre.l@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="L.", first_name="Nina", email="nina.l@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="N.", first_name="Corentin", email="corentin.n@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="P.", first_name="Flavie", email="flavie.p@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="T.", first_name="Adrien", email="adrien.t@example.com", consumption_history=[], current_plan=""),
        Customer(last_name="Z.", first_name="Rawend", email="rawend.z@example.com", consumption_history=[], current_plan=""),
    ]

    nb_months = 60
    for customer in customers:
        profile = random.choice(profiles)
        customer.current_plan = profile["name"]
        base_hour = profile["hour_volume"]
        base_sms = profile["sms_volume"]
        base_gb = profile["gb_volume"]
        direction = 1
        current_year = 2020
        current_month = 1
        
        for i in range(nb_months):
            date = datetime.date(current_year, current_month, 1)
            
            current_month += 1

            if current_month > 12:
                current_month = 1
                current_year += 1

            if random.random() < 0.: 
                direction *= -1

            base_hour += random.uniform(0, profile["variation"]["hour"]) * direction + random.uniform(-1, 1)
            base_sms += random.randint(0, profile["variation"]["sms"]) * direction + random.randint(-2, 2)
            base_gb += random.uniform(0, profile["variation"]["gb"]) * direction + random.uniform(-0.3, 0.3)

            consumption = Consumption(
                name=profile["name"],
                date=date,
                hour_volume=round(base_hour, 2),
                sms_volume=base_sms,
                gb_volume=round(base_gb, 2),
                price=profile["price"]
            )
            
            customer.consumption_history.append(consumption)

    plans = [
        Plan(name="Forfait 2€", hour_volume=2, sms_volume=-1, gb_volume=0.50, price=2.00, type="INTERNE"),
        Plan(name="Série Free", hour_volume=-1, sms_volume=-1, gb_volume=110, price=8.99, type="INTERNE"),
        Plan(name="Forfait Free 5G", hour_volume=-1, sms_volume=-1, gb_volume=350, price=19.99, type="INTERNE"),
    ]

    with Session(engine) as session:
        session.add_all(customers + plans)
        session.commit()

if __name__ == "__main__":
    load_fixtures()