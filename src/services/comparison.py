from src.models.customer import Customer
from src.models.plan import Plan
from src.models.consumption import Consumption

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Comparison:

    engine = create_engine('mysql+mysqlconnector://root:@localhost/planify')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    plans = session.query(Plan).all()
    customers = session.query(Customer).all()
    consumptions = session.query(Consumption).all()


    def calculate_average_consumption_gb(self, customer):
        total_comsumption_gb = 0
        for consumption in customer.consumption_history:
            total_comsumption_gb += consumption.gb_volume
        average_gb = total_comsumption_gb / len(customer.consumption_history)
        return round(average_gb, 2)
        

    def calculate_average_consumption_hour(self, customer):
        total_comsumption = 0
        for consumption in customer.consumption_history:
            total_comsumption += consumption.hour_volume
        average = total_comsumption / len(customer.consumption_history)
        return round(average, 2)
    

    def calculate_average_consumption_sms(self, customer):
        total_comsumption = 0
        for consumption in customer.consumption_history:
            total_comsumption += consumption.sms_volume
        average = total_comsumption / len(customer.consumption_history)
        return round(average, 2)
    

    def get_annual_cost(self, customer):
        total_cost = 0
        first_year = None
        for consumption in customer.consumption_history:
            if first_year == None:
                first_year = consumption.date.year
            if consumption.date.year == first_year:
                total_cost += consumption.price
        return round(total_cost, 2)
    

    def get_annual_consumption_gb(self, customer):
        total_comsumption = 0
        for consumption in customer.consumption_history:
            total_comsumption += consumption.gb_volume
        return round(total_comsumption, 2)
    

    def count_customers(self):
        return len(self.customers)
    

    def get_average_consumption_all_customers(self):
        total_gb = 0
        for customer in self.customers:
            total_gb += self.calculate_average_consumption_gb(customer)
        average_gb_all_customers = total_gb / len(self.customers)
        return round(average_gb_all_customers, 2)
    

    def get_most_popular_plan(self):
        plan_count = []
        
        for customer in self.customers:
            plan_name = customer.current_plan
            
            plan_exists = False
            
            for item in plan_count:
                if item[0] == plan_name:
                    item[1] = item[1] + 1  
                    plan_exists = True
                    break
            
            if plan_exists == False:
                plan_count.append([plan_name, 1])
        
        most_popular = plan_count[0][0]
        highest_count = plan_count[0][1]
        
        for item in plan_count:
            plan_name = item[0]
            count = item[1]
            
            if count > highest_count:
                most_popular = plan_name
                highest_count = count
        
        return most_popular
    

    def get_annual_average_consumption_all_clients(self):
        years = []
        
        for customer in self.customers:
            for consumption in customer.consumption_history:
                year = consumption.date.year
                
                if year not in years:
                    years.append(year)
                
        average_gb = []
        average_sms = []
        average_hour = []
        
        for year in years:
            total_gb = 0
            total_sms = 0
            total_hour = 0
            counter = 0
            
            for customer in self.customers:
                for consumption in customer.consumption_history:
                    
                    if consumption.date.year == year:
                        total_gb = total_gb + consumption.gb_volume
                        total_sms = total_sms + consumption.sms_volume
                        total_hour = total_hour + consumption.hour_volume
                        counter = counter + 1
            
            if counter > 0:
                avg_gb = total_gb / counter
                avg_sms = total_sms / counter
                avg_hour = total_hour / counter
                
                average_gb.append(round(avg_gb, 2))
                average_sms.append(round(avg_sms, 2))
                average_hour.append(round(avg_hour, 2))
        
        return {
            "Go": average_gb,
            "SMS": average_sms,
            "Heure": average_hour
        }


    def popular_plans(self):
        list_plans = []
        for customer in self.customers:
            list_plans.append(customer.current_plan)

        total = len(list_plans)

        plan1_count = list_plans.count("SFR Série Free")
        plan2_count = list_plans.count("SFR Forfait Free 5G")
        plan3_count = list_plans.count("SFR Forfait 2€")

        return {
            "SFR Série Free": (plan1_count / total) * 100,
            "SFR Forfait Free 5G": (plan2_count / total) * 100, 
            "SFR Forfait 2€": (plan3_count / total) * 100
        }
    

    def get_consumption_history_data(self, customer):
        list_consumptions = []
        for c in customer.consumption_history:
            ligne = {
                "Date": c.date,
                "Volume heure": c.hour_volume,
                "Volume SMS": c.sms_volume,
                "Volume Go": c.gb_volume
            }
            list_consumptions.append(ligne)
        return list_consumptions
    

    def best_plan_recommendation(self, customer):
        avg_consumption = self.calculate_average_consumption_gb(customer)       
        chosen_plan = None
        
        for plan in self.plans:
            if plan.gb_volume >= avg_consumption:
                chosen_plan = plan
                break 
        
        if chosen_plan is None:
            chosen_plan = self.plans[0]  
            
            for plan in self.plans:
                if plan.gb_volume > chosen_plan.gb_volume:
                    chosen_plan = plan
        
        result = f"{chosen_plan.name} ({chosen_plan.gb_volume} Go)"
        return result