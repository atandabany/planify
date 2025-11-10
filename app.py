import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import altair as alt
import pandas as pd

from src.models.customer import Customer
from src.models.plan import Plan
from src.services.comparison import Comparison


# Connexion à la bdd
engine = create_engine('mysql+mysqlconnector://root:@localhost/planify')
Session = sessionmaker(bind=engine)
session = Session()


# Appel des données de la bdd
plans = session.query(Plan).all()
customers = session.query(Customer).all()
comparison = Comparison()


#st.balloons()
#st.snow()
st.title("Planify")
st.caption("Analyse et recommandation de forfaits personnalisés.")

tab1, tab2 = st.tabs(["Accueil", "Client"])

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        container1 = st.container(border=True)
        container1.write(f"Nombre de clients : **{comparison.count_customers()}**")

    with col2:
        container2 = st.container(border=True)
        container2.write(f"Conso moyenne GO : **{comparison.get_average_consumption_all_customers()}**")

    with col3:
        container3 = st.container(border=True)
        container3.write(f"Populaire : **{comparison.get_most_popular_plan()}**")


    col4, col5 = st.columns(2)

    with col4:
        container4 = st.container(border=True)
        with container4:
            st.write("Consommation moyenne annuelle")
            data = comparison.get_annual_average_consumption_all_clients()
            df = pd.DataFrame(data)
            st.bar_chart(df)

    with col5:
        container5 = st.container(border=True)
        with container5:
            st.write("Distribution des forfaits")
            plan_percentages = comparison.popular_plans()
            df = pd.DataFrame(list(plan_percentages.items()), columns=["Forfait", "Pourcentage"])
            chart = alt.Chart(df).mark_arc().encode(
                theta='Pourcentage',
                color=alt.Color('Forfait', legend=alt.Legend(orient='bottom'), title=None)
            )
            st.altair_chart(chart, use_container_width=True)


with tab2:
    list_names = []
    for customer in customers:
        customer_name = f"{customer.get_last_name()} {customer.get_first_name()}"
        list_names.append(customer_name)

    option = st.selectbox(
        "Selectionnez un client : ",
        list_names,
    )

    selected_customer = None
    for customer in customers:
        customer_name = f"{customer.get_last_name()} {customer.get_first_name()}"
        if customer_name == option:
            selected_customer = customer
            break


    col6, col7 = st.columns(2)

    with col6:
        if selected_customer:
            container1 = st.container(border=True)
            container2 = st.container(border=True)
            container1.write(f"Email : {selected_customer.get_email()}")
            container2.write(f"Forfait actuel : {selected_customer.get_current_plan()}")

    with col7:
        container6 = st.container(border=True)
        container7 = st.container(border=True)
        container6.write(f":green[Recommandation forfait : {comparison.best_plan_recommendation(selected_customer)}]")
        container7.write(f":red[Dépense annuel : {comparison.get_annual_cost(selected_customer)} €]")


    st.divider()
    st.write("Consommation moyenne du client sur 5 ans :")


    col8, col9, col10 = st.columns(3)

    with col8:
        container8 = st.container(border=True)
        container8.write(f"Conso Go : **{comparison.calculate_average_consumption_gb(selected_customer)}**")

    with col9:
        container9 = st.container(border=True)
        container9.write(f"Conso SMS : **{comparison.calculate_average_consumption_sms(selected_customer)}**")

    with col10:
        container10 = st.container(border=True)
        container10.write(f"Conso Heures : **{comparison.calculate_average_consumption_hour(selected_customer)}**")  


    st.write("Évolution des consommations")

    liste_consommations = comparison.get_consumption_history_data(selected_customer)
    df = pd.DataFrame(liste_consommations)

    chart = alt.Chart(df).transform_fold(
        ['Volume heure', 'Volume SMS', 'Volume Go'],
        as_=['Type', 'Valeur']
    ).mark_area().encode(
        x='Date:T',
        y='Valeur:Q',
        color='Type:N'
    )

    st.altair_chart(chart, use_container_width=True)
    #st.dataframe(df)
    st.divider()


st.caption("© 2025 Planify — Application appartenant à l’entreprise Free - Groupe iliad.")
st.caption(" Tous droits réservés. Toute reproduction, distribution ou utilisation non autorisée est strictement interdite.")
st.caption("Développé par Adrien Tandabany dans le cadre d'un projet professionnel.")