import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  
import openai
from openai import OpenAI

# Configurer le style Seaborn
sns.set_theme(style="whitegrid", palette="pastel")

def calculate_savings(P, E, n_years, r_annual, months_between_savings):
    periods_per_year = 12 / months_between_savings
    r_periodic = r_annual / periods_per_year
    capital_accumulated = [P]
    savings_accumulated = [P]
    interest_accumulated = [0]
    
    for year in range(1, n_years + 1):
        for period in range(int(periods_per_year)):
            interest = P * r_periodic
            P += interest + E
        capital_accumulated.append(P)
        savings_accumulated.append(savings_accumulated[-1] + E * periods_per_year)
        interest_accumulated.append(P - savings_accumulated[-1])
    
    return np.arange(0, n_years + 1), capital_accumulated, savings_accumulated, interest_accumulated, P

def calculate_mortgage(P, annual_interest_rate, years):
    n = years * 12
    r = annual_interest_rate / 12
    M = P * (r * (1 + r)**n) / ((1 + r)**n - 1)
    
    monthly_payment = np.array([M] * n)
    principal_paid = np.zeros(n)
    interest_paid = np.zeros(n)
    remaining_balance = np.zeros(n)
    total_interest = 0
    
    for month in range(n):
        interest = (P * r)
        principal = M - interest
        P -= principal
        
        interest_paid[month] = interest
        principal_paid[month] = principal
        remaining_balance[month] = P
        total_interest += interest
        
    return monthly_payment, principal_paid, interest_paid, remaining_balance, total_interest, M

def plot_savings(x, y1, y2, y3, title, labels):
    plt.figure(figsize=(12, 8))
    sns.lineplot(x=x, y=y1, label=labels[0], color='blue', marker="o", linewidth=3, markersize=10)
    sns.lineplot(x=x, y=y2, label=labels[1], color='green', marker="o", dashes=(5, 2))
    sns.lineplot(x=x, y=y3, label=labels[2], color='red', marker="o", dashes=(5, 2))
    plt.title(title)
    plt.xlabel('Années')
    plt.ylabel('Montant (€)')
    plt.legend()
    return plt

def plot_mortgage(years, remaining_balance, interest_paid, principal_paid, annual_total_paid, title):
    plt.figure(figsize=(12, 8))
    sns.lineplot(x=years, y=remaining_balance, label='Solde Restant', color='skyblue', marker="o", linewidth=3, markersize=10)
    sns.lineplot(x=years, y=np.cumsum(annual_total_paid), label='Total Payé', color='blue', marker="o", linewidth=3, markersize=10)
    sns.lineplot(x=years, y=np.cumsum(interest_paid), label='Total Intérêts Payés', color='salmon', marker="o", dashes=(5, 2))
    sns.lineplot(x=years, y=np.cumsum(principal_paid), label='Principal Payé', color='lightgreen', marker="o", dashes=(5, 2))
    plt.title(title)
    plt.xlabel('Années')
    plt.ylabel('Montant (€)')
    plt.legend()
    return plt


class App:
    def __init__(self):
        # Streamlit interface
        st.title('Gestion patrimoniale')

        # Création des onglets
        tab1, tab2 = st.tabs(["Épargne", "Achat"])

        with tab1:
            st.header('Paramètres de l\'épargne')
            with st.form("savings_form"):
                P_savings = st.number_input('Placement de départ (€)', value=10000, step=1000)
                E_savings = st.number_input('Épargne périodique (€)', value=500, step=100)
                months_between_savings = st.selectbox('Fréquence des versements', options=[1, 3, 6, 12], format_func=lambda x: f"{int(12/x)} fois par an")
                n_years_savings = st.slider('Durée du placement (années)', 1, 30, 20)
                r_annual_savings = st.slider('Taux de rendement annuel (%)', 0.01, 0.15, 0.06)
                submit_savings = st.form_submit_button("Calculer")
            
            if submit_savings:
                x_savings, capital_accumulated, savings_accumulated, interest_accumulated, final_capital = calculate_savings(P_savings, E_savings, n_years_savings, r_annual_savings, months_between_savings)
                plt = plot_savings(x_savings, capital_accumulated, savings_accumulated, interest_accumulated, 'Évolution de l\'épargne au fil des années', ['Capital Total', 'Participation Épargne', 'Participation Intérêts'])
                st.pyplot(plt)
                st.write(f"Capital final après {n_years_savings} ans : {final_capital:,.2f}€".replace(',', ' '))  # Formatting for thousands separator

        with tab2:
            st.header('Paramètres de l\'achat immobilier')
            with st.form("mortgage_form"):
                P_mortgage = st.number_input('Montant du prêt (€)', value=316000, step=1000, key="mortgage_amount")
                st.caption("Pensez à compter les frais de notaire et de garantie dans le montant du prêt. Par exemple pour un bien à 350 000€, comptez 10% de frais soit 35 000€. Vous devrez donc emprunter 350 000€ + 35 000€ = 385 000€. Si vous avez un apport de 20 000€, vous devrez emprunter 365 000€.")
                annual_interest_rate_mortgage = st.slider('Taux d\'intérêt annuel (%)', 0.01, 0.10, 0.042, key="mortgage_rate")
                years_mortgage = st.slider('Durée du prêt (années)', 1, 30, 25, key="mortgage_years")
                submit_mortgage = st.form_submit_button("Calculer")
            
            if submit_mortgage:
                monthly_payment, principal_paid, interest_paid, remaining_balance, total_interest, M = calculate_mortgage(P_mortgage, annual_interest_rate_mortgage, years_mortgage)
                months = np.arange(1, years_mortgage * 12 + 1)

                # Conversion des données mensuelles en annuelles pour le tracé
                years_arr = np.arange(1, years_mortgage + 1)
                annual_interest_paid = np.array([sum(interest_paid[i*12:(i+1)*12]) for i in range(years_mortgage)])
                annual_principal_paid = np.array([sum(principal_paid[i*12:(i+1)*12]) for i in range(years_mortgage)])

                # Le solde restant à la fin de chaque année (prendre le dernier mois de chaque année)
                annual_remaining_balance = remaining_balance[11::12]
                annual_total_paid = annual_principal_paid + annual_interest_paid

                plt = plot_mortgage(years_arr, annual_remaining_balance, annual_interest_paid, annual_principal_paid, annual_total_paid, 'Échéancier du prêt sur 20 ans (Résumé Annuel)')
                st.pyplot(plt)
                st.write(f"Total des intérêts payés sur la période du prêt : {total_interest:,.2f}€".replace(',', ' '))  # Formatting for thousands separator
                st.write(f"Échéance mensuelle : {M:,.2f}€".replace(',', ' '))


        st.divider()

        st.header('Posez vos questions à l\'assistant virtuel')

        # Déterminez l'onglet actif et si une simulation a été effectuée
        onglet_actif = "Épargne" if tab1 else "Achat" if tab2 else "Non défini"
        simulation_effectuee = submit_savings if tab1 else submit_mortgage if tab2 else False

        # Si une simulation n'a pas été effectuée, faites-le pour l'utilisateur
        if not simulation_effectuee:
            if onglet_actif == "Épargne":
                # Appel de la fonction calculate_savings avec des valeurs par défaut ou celles saisies par l'utilisateur
                x_savings, capital_accumulated, savings_accumulated, interest_accumulated, final_capital = calculate_savings(P_savings, E_savings, n_years_savings, r_annual_savings, months_between_savings)
                preprompt = f"""
                Tu es un assistant virtuel spécialisé dans le conseil financier, particulièrement expérimenté dans les stratégies d'épargne. Tu aides les utilisateurs à optimiser leurs plans d'épargne 
                en fonction de leurs objectifs à long terme. Actuellement, tu es en train d'assister un utilisateur qui envisage un plan d'épargne. 
                
                Voici les détails de sa simulation :
                - Placement initial : {P_savings}€
                - Épargne périodique : {E_savings}€ tous les {months_between_savings} mois
                - Durée du placement : {n_years_savings} ans
                - Taux de rendement annuel estimé : {r_annual_savings*100}%

                Voici les résultats : 
                - Capital final après {n_years_savings} ans : {final_capital}€
                - Épargne totale : {savings_accumulated[-1]}€
                - Intérêts totaux : {interest_accumulated[-1]}€
                - Capital total : {capital_accumulated[-1]}€

                L'utilisateur cherche à comprendre comment maximiser le rendement de son épargne au fil des ans et souhaite des conseils sur les meilleures stratégies d'épargne pour atteindre ses objectifs financiers. 
                Ton rôle est de fournir des analyses, des recommandations personnalisées, et de répondre à ses questions de manière claire et informative, tout en utilisant un langage accessible et amical. 
                Pense à souligner l'importance de la discipline d'épargne, des avantages du rendement composé, et à proposer des ajustements stratégiques si nécessaire.
                """
            elif onglet_actif == "Achat":
                # Appel de la fonction calculate_mortgage avec des valeurs par défaut ou celles saisies par l'utilisateur
                monthly_payment, principal_paid, interest_paid, remaining_balance, total_interest, M = calculate_mortgage(P_mortgage, annual_interest_rate_mortgage, years_mortgage)
                preprompt = f"""
                Tu es un expert immobilier virtuel, doté d'une grande expertise dans le domaine des achats immobiliers. Tu assistes les utilisateurs dans l'évaluation de leurs options d'achat immobilier, 
                en tenant compte de leurs capacités financières et de leurs objectifs à long terme. 
                
                Voici les détails de la simulation d'achat de l'utilisateur :
                - Montant du prêt : {P_mortgage}€
                - Taux d'intérêt annuel : {annual_interest_rate_mortgage*100}%
                - Durée du prêt : {years_mortgage} ans
                - Échéance mensuelle calculée : {M}€
                - Total des intérêts payés sur la période du prêt : {total_interest}€

                L'utilisateur souhaite des conseils sur l'achat immobilier, notamment sur la manière de choisir le meilleur prêt immobilier, d'évaluer le coût total de l'achat, 
                et de planifier son budget à long terme. Ton rôle est d'offrir des insights pertinents sur le marché immobilier, des stratégies pour négocier les meilleures conditions de prêt, 
                et d'expliquer les implications financières de l'achat immobilier. Ta réponse doit être informative, personnalisée, et exprimée dans un langage compréhensible pour 
                faciliter la prise de décision de l'utilisateur.
                """

        openai_api_key = st.text_input("Entrez votre clé API OpenAI", type="password")

        # .streamlit/secrets.toml
        client = OpenAI(api_key=openai_api_key)

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-4"

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": preprompt}]

            first_message = {"role": "assistant", "content": f"Bonjour, je suis votre conseiller financier virtuel. Comment puis-je vous aider aujourd'hui ?"}
            st.session_state.messages.append(first_message)

        for message in st.session_state.messages:
            if "assistant" in message["role"] or "user" in message["role"]:
                with st.chat_message(message["role"]):
                        st.markdown(message["content"]) 

        if prompt := st.chat_input("Message à l'assistant virtuel"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): 
                st.markdown(prompt)

                # print(num_tokens_from_string(preprompt+prompt, "cl100k_base"))

            if not openai_api_key:
                st.warning("Veuillez entrer une clé API pour continuer.")
            else:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    for response in client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        # messages=[
                        #     {"role": "user", "content": preprompt+prompt}
                        #     for m in st.session_state.messages
                        # ],
                        stream=True,
                    ):
                        full_response += (response.choices[0].delta.content or "")
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            all_msgs = [m["content"] for m in st.session_state.messages]
            all_msgs = " ".join(all_msgs)

### Run app
app = App()