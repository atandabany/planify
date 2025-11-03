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
            if first_year is None:
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
    

    #A voir
    def get_most_popular_plan(self):
        plan_count = {}
        for customer in self.customers:
            plan_name = customer.current_plan
            if plan_name in plan_count:
                plan_count[plan_name] += 1
            else:
                plan_count[plan_name] = 1
        most_popular_plan = max(plan_count, key=plan_count.get)
        return most_popular_plan
    

    def get_annual_average_consumption_all_clients(self):
        # 1. Récupérer toutes les années
        annees = []
        for customer in self.customers:
            for c in customer.consumption_history:
                if c.date.year not in annees:
                    annees.append(c.date.year)

        annees.sort()

        # 2. Calculer la moyenne par année
        moyenne_gb = []
        moyenne_sms = []
        moyenne_hour = []

        for year in annees:
            total_gb = 0
            total_sms = 0
            total_hour = 0
            compteur = 0

            for customer in self.customers:
                for c in customer.consumption_history:
                    if c.date.year == year:
                        total_gb += c.gb_volume
                        total_sms += c.sms_volume
                        total_hour += c.hour_volume 
                        compteur += 1

            if compteur > 0:
                moyenne_gb.append(round(total_gb / compteur, 2))
                moyenne_sms.append(round(total_sms / compteur, 2))
                moyenne_hour.append(round(total_hour / compteur, 2))

        # 3. Retourner les données
        return {
            "Go": moyenne_gb,
            "SMS": moyenne_sms,
            "Heure": moyenne_hour  
        }

    def popular_plans(self):
        list_plans = []
        for customer in self.customers:
            # Ajouter directement le plan (pas d'itération)
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
        liste_consommations = []
        for c in customer.consumption_history:
            ligne = {
                "Date": c.date,
                "Volume heure": c.hour_volume,
                "Volume SMS": c.sms_volume,
                "Volume Go": c.gb_volume
            }
            liste_consommations.append(ligne)
        return liste_consommations
    

    # Consommation min / max
    # Évolution (%) par rapport à l’année précédente
    # Forfait recommandé + prix comparé au forfait actuel